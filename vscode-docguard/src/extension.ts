import * as vscode from 'vscode';
import { DocGuardClient } from './docguardClient';
import { workspaceHasGitChanges } from './gitDiffProvider';
import { DocGuardPanelProvider } from './panelProvider';
import { applyPatch } from './patchApplier';
import { DocGuardStatusBar } from './statusBar';
import { DocGuardResult } from './types';

let lastResult: DocGuardResult | undefined;
let debounce: NodeJS.Timeout | undefined;

export function activate(context: vscode.ExtensionContext): void {
  const client = new DocGuardClient(context.extensionUri);
  const panel = new DocGuardPanelProvider(context.extensionUri);
  const status = new DocGuardStatusBar();
  context.subscriptions.push(status, vscode.window.registerWebviewViewProvider('docguard.panel', panel));

  async function analyze(): Promise<void> {
    const folder = vscode.workspace.workspaceFolders?.[0];
    if (!folder) {
      void vscode.window.showWarningMessage('Open a workspace folder before running DocGuard.');
      return;
    }
    panel.showLoading();
    status.setAnalyzing();
    try {
      await client.checkRuntime(folder);
      lastResult = await client.analyzeWorkspace(folder);
      panel.showResult(lastResult);
      if (lastResult.status === 'error') {
        status.setError();
      } else if (lastResult.docs_update_required) {
        status.setNeeded();
      } else {
        status.setNoUpdate();
        void vscode.window.showInformationMessage('No documentation update required.');
      }
    } catch (error) {
      status.setError();
      panel.showResult({
        status: 'error',
        docs_update_required: false,
        doc_category: 'no_update',
        target_doc_file: null,
        target_section: 'Documentation',
        scenario_type: 'extension_error',
        confidence: 0,
        reason: 'Extension runtime call failed.',
        patch: null,
        diagnostics: { changed_files: [], model_used: 'none', classifier_architecture: 'none', input_mode: 'none', runtime_ms: 0 },
        error_message: String(error)
      });
    }
  }

  context.subscriptions.push(
    vscode.commands.registerCommand('docguard.analyzeWorkspace', analyze),
    vscode.commands.registerCommand('docguard.analyzeCurrentFile', analyze),
    vscode.commands.registerCommand('docguard.openPanel', () => panel.reveal()),
    vscode.commands.registerCommand('docguard.startRuntime', () => vscode.window.showInformationMessage('DocGuard CLI runtime is ready.')),
    vscode.commands.registerCommand('docguard.stopRuntime', () => vscode.window.showInformationMessage('DocGuard CLI runtime stopped.')),
    vscode.commands.registerCommand('docguard.ignoreSuggestion', () => {
      lastResult = undefined;
      panel.clear();
      status.setReady();
    }),
    vscode.commands.registerCommand('docguard.applyPatch', async () => {
      const folder = vscode.workspace.workspaceFolders?.[0];
      if (!folder || !lastResult?.patch) {
        return;
      }
      const confirm = await vscode.window.showWarningMessage('Apply DocGuard documentation patch?', { modal: true }, 'Apply Patch');
      if (confirm !== 'Apply Patch') {
        return;
      }
      await applyPatch(folder, lastResult.patch);
      void vscode.window.showInformationMessage(`DocGuard updated ${lastResult.patch.file}.`);
      await analyze();
    })
  );

  context.subscriptions.push(vscode.workspace.onDidSaveTextDocument(() => {
    const enabled = vscode.workspace.getConfiguration('docguard').get<boolean>('autoAnalyzeOnSave', false);
    const folder = vscode.workspace.workspaceFolders?.[0];
    if (!enabled || !folder) {
      return;
    }
    if (debounce) {
      clearTimeout(debounce);
    }
    debounce = setTimeout(() => {
      void workspaceHasGitChanges(folder).then(hasChanges => {
        if (hasChanges) {
          void analyze();
        }
      });
    }, 1500);
  }));
}

export function deactivate(): void {}

