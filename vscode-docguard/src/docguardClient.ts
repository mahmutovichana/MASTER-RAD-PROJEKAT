import * as cp from 'child_process';
import * as path from 'path';
import * as vscode from 'vscode';
import { DocGuardResult } from './types';

export class DocGuardClient {
  private readonly output: vscode.OutputChannel;

  constructor(private readonly extensionUri: vscode.Uri) {
    this.output = vscode.window.createOutputChannel('DocGuard');
  }

  async analyzeWorkspace(workspace: vscode.WorkspaceFolder): Promise<DocGuardResult> {
    const config = vscode.workspace.getConfiguration('docguard');

    const pythonPath = config.get<string>('pythonPath', 'python');
    const inputMode = config.get<string>('modelInputMode', 'raw_diff_plus_docs');
    const architecture = config.get<string>('classifierArchitecture', 'staged');

    // extensionUri points to:
    // ...\MASTER RAD PROJEKAT\vscode-docguard
    //
    // repoRoot must be:
    // ...\MASTER RAD PROJEKAT
    const repoRoot = path.resolve(this.extensionUri.fsPath, '..');
    const workspacePath = workspace.uri.fsPath;

    const args = [
      '-m',
      'docguard_runtime.runtime_cli',
      'analyze-workspace',
      '--workspace',
      workspacePath,
      '--format',
      'json',
      '--input-mode',
      inputMode,
      '--classifier-architecture',
      architecture
    ];

    return this.runJson(pythonPath, args, repoRoot, workspacePath);
  }

  async checkRuntime(workspace: vscode.WorkspaceFolder): Promise<void> {
    const config = vscode.workspace.getConfiguration('docguard');

    const architecture = config.get<string>('classifierArchitecture', 'staged');
    const inputMode = config.get<string>('modelInputMode', 'raw_diff_plus_docs');

    const repoRoot = path.resolve(this.extensionUri.fsPath, '..');

    const modelPath = path.join(
      repoRoot,
      'models',
      'hf_v0_4',
      inputMode,
      `embedding_classifier${architecture === 'staged' ? '_staged' : ''}.joblib`
    );

    const runtimePath = path.join(repoRoot, 'docguard_runtime', 'runtime_cli.py');

    this.output.appendLine('=== DocGuard Runtime Check ===');
    this.output.appendLine(`repoRoot: ${repoRoot}`);
    this.output.appendLine(`workspace: ${workspace.uri.fsPath}`);
    this.output.appendLine(`modelPath: ${modelPath}`);
    this.output.appendLine(`runtimePath: ${runtimePath}`);

    try {
      await vscode.workspace.fs.stat(vscode.Uri.file(modelPath));
    } catch {
      void vscode.window.showWarningMessage(
        'DocGuard classifier model is missing. Train DocGuard classifier first.',
        'Show Command'
      ).then(choice => {
        if (choice) {
          void vscode.window.showInformationMessage(
            'python -m docguard_hf_classifier.cli train-embeddings --version v0_4 --model sentence-transformers/all-MiniLM-L6-v2 --input-mode raw_diff_plus_docs --classifier-architecture staged'
          );
        }
      });
    }

    await vscode.workspace.fs.stat(vscode.Uri.file(runtimePath));
  }

  private runJson(
    command: string,
    args: string[],
    cwd: string,
    workspacePath: string
  ): Promise<DocGuardResult> {
    return new Promise((resolve, reject) => {
      const env = {
        ...process.env,
        PYTHONPATH: `${cwd}${path.delimiter}${process.env.PYTHONPATH ?? ''}`
      };

      this.output.appendLine('');
      this.output.appendLine('=== DocGuard Runtime Command ===');
      this.output.appendLine(`command: ${command}`);
      this.output.appendLine(`args: ${JSON.stringify(args)}`);
      this.output.appendLine(`cwd: ${cwd}`);
      this.output.appendLine(`workspacePath: ${workspacePath}`);
      this.output.appendLine(`PYTHONPATH: ${env.PYTHONPATH}`);

      const child = cp.spawn(command, args, {
        cwd,
        env,
        shell: false
      });

      let stdout = '';
      let stderr = '';

      child.stdout.on('data', chunk => {
        stdout += chunk.toString();
      });

      child.stderr.on('data', chunk => {
        stderr += chunk.toString();
      });

      child.on('error', error => {
        this.output.appendLine('');
        this.output.appendLine('=== DocGuard Process Error ===');
        this.output.appendLine(String(error));
        reject(error);
      });

      child.on('close', code => {
        this.output.appendLine('');
        this.output.appendLine('=== DocGuard Runtime Result ===');
        this.output.appendLine(`exit code: ${code}`);
        this.output.appendLine(`stdout: ${stdout}`);
        this.output.appendLine(`stderr: ${stderr}`);

        if (code !== 0) {
          reject(new Error(stderr || stdout || `DocGuard runtime failed with exit code ${code}`));
          return;
        }

        try {
          const parsed = JSON.parse(stdout.trim()) as DocGuardResult;
          resolve(parsed);
        } catch (error) {
          this.output.appendLine('');
          this.output.appendLine('=== DocGuard JSON Parse Error ===');
          this.output.appendLine(String(error));
          reject(new Error(stderr || stdout || String(error)));
        }
      });
    });
  }
}