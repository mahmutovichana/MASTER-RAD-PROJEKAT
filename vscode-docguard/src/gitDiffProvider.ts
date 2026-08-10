import * as cp from 'child_process';
import * as vscode from 'vscode';

export async function workspaceHasGitChanges(folder: vscode.WorkspaceFolder): Promise<boolean> {
  return new Promise(resolve => {
    cp.exec('git diff --quiet && git diff --cached --quiet', { cwd: folder.uri.fsPath }, error => {
      resolve(Boolean(error));
    });
  });
}

