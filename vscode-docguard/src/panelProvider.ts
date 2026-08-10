import * as vscode from 'vscode';
import { DocGuardResult } from './types';

type PanelState = 'empty' | 'loading' | 'result' | 'error';

export class DocGuardPanelProvider implements vscode.WebviewViewProvider {
  private view?: vscode.WebviewView;
  private state: PanelState = 'empty';
  private result?: DocGuardResult;

  constructor(private readonly extensionUri: vscode.Uri) {}

  resolveWebviewView(webviewView: vscode.WebviewView): void {
    this.view = webviewView;
    webviewView.webview.options = { enableScripts: true, localResourceRoots: [this.extensionUri] };
    webviewView.webview.onDidReceiveMessage(message => {
      if (message.command === 'apply') {
        void vscode.commands.executeCommand('docguard.applyPatch');
      } else if (message.command === 'ignore') {
        void vscode.commands.executeCommand('docguard.ignoreSuggestion');
      } else if (message.command === 'rerun') {
        void vscode.commands.executeCommand('docguard.analyzeWorkspace');
      }
    });
    this.render();
  }

  showLoading(): void {
    this.state = 'loading';
    this.render();
  }

  showResult(result: DocGuardResult): void {
    this.state = result.status === 'error' ? 'error' : 'result';
    this.result = result;
    this.render();
  }

  clear(): void {
    this.state = 'empty';
    this.result = undefined;
    this.render();
  }

  reveal(): void {
    void this.view?.show?.(true);
  }

  private render(): void {
    if (!this.view) {
      return;
    }
    const css = this.view.webview.asWebviewUri(vscode.Uri.joinPath(this.extensionUri, 'media', 'main.css'));
    this.view.webview.html = `<!doctype html><html><head><link rel="stylesheet" href="${css}"></head><body>${this.body()}<script>
      const vscode = acquireVsCodeApi();
      document.querySelectorAll('[data-command]').forEach(btn => btn.addEventListener('click', () => vscode.postMessage({command: btn.dataset.command})));
    </script></body></html>`;
  }

  private body(): string {
    if (this.state === 'loading') {
      return '<main><h2>Analyzing workspace changes...</h2></main>';
    }
    if (this.state === 'empty' || !this.result) {
      return '<main><h2>DocGuard</h2><p>Run DocGuard to analyze current changes.</p><button data-command="rerun">Run Analysis</button></main>';
    }
    if (this.result.status === 'error') {
      return `<main><h2 class="error">DocGuard Error</h2><p>${escapeHtml(this.result.error_message || 'Unknown error')}</p><button data-command="rerun">Try Again</button></main>`;
    }
    if (!this.result.docs_update_required) {
      return `<main><h2 class="ok">No documentation update required</h2><p>${escapeHtml(this.result.reason)}</p><button data-command="rerun">Re-run Analysis</button></main>`;
    }
    const patch = this.result.patch;
    return `<main>
      <h2 class="warn">Documentation update needed</h2>
      <dl>
        <dt>Target file</dt><dd>${escapeHtml(this.result.target_doc_file || '')}</dd>
        <dt>Scenario</dt><dd>${escapeHtml(this.result.scenario_type)}</dd>
        <dt>Category</dt><dd>${escapeHtml(this.result.doc_category)}</dd>
        <dt>Confidence</dt><dd>${this.result.confidence.toFixed(2)}</dd>
        <dt>Reason</dt><dd>${escapeHtml(this.result.reason)}</dd>
      </dl>
      <h3>Patch preview</h3>
      <pre>${escapeHtml(patch?.preview || '')}</pre>
      <button data-command="apply">Apply Patch</button>
      <button data-command="ignore">Ignore</button>
      <button data-command="rerun">Re-run Analysis</button>
    </main>`;
  }
}

function escapeHtml(value: string): string {
  return value.replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[ch] || ch));
}

