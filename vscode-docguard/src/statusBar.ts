import * as vscode from 'vscode';

export class DocGuardStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);

  constructor() {
    this.item.command = 'docguard.openPanel';
    this.setReady();
    this.item.show();
  }

  dispose(): void {
    this.item.dispose();
  }

  setReady(): void {
    this.item.text = 'DocGuard: Ready';
  }

  setAnalyzing(): void {
    this.item.text = 'DocGuard: Analyzing...';
  }

  setNeeded(): void {
    this.item.text = 'DocGuard: Docs update needed';
  }

  setNoUpdate(): void {
    this.item.text = 'DocGuard: No docs update';
  }

  setError(): void {
    this.item.text = 'DocGuard: Error';
  }
}

