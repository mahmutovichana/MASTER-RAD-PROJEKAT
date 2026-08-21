import * as cp from 'child_process';
import * as path from 'path';
import * as vscode from 'vscode';
import { DocGuardResult } from './types';

export class DocGuardClient {
  private readonly output: vscode.OutputChannel;

  constructor(private readonly extensionUri: vscode.Uri) {
    this.output = vscode.window.createOutputChannel('DocGuard');
  }

  async analyzeWorkspace(workspace: vscode.WorkspaceFolder, patchBackendOverride?: string): Promise<DocGuardResult> {
    const config = vscode.workspace.getConfiguration('docguard');

    const pythonPath = config.get<string>('pythonPath', 'python');
    const inputMode = config.get<string>('modelInputMode', 'raw_diff_plus_docs');
    const architecture = config.get<string>('classifierArchitecture', 'hybrid_router');
    const patchBackend = patchBackendOverride || config.get<string>('patchBackend', 'deterministic');
    const patchModel = config.get<string>('patchModel', 'Qwen/Qwen2.5-1.5B-Instruct');
    const patchMaxNewTokens = config.get<number>('patchMaxNewTokens', 192);
    const patchTemperature = config.get<number>('patchTemperature', 0.1);
    const analysisBackend = config.get<string>('analysisBackend', 'hybrid');
    const analysisModel = config.get<string>('analysisModel', patchModel);
    const analysisMaxNewTokens = config.get<number>('analysisMaxNewTokens', 256);
    const analysisTemperature = config.get<number>('analysisTemperature', 0.0);

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
      architecture,
      '--analysis-backend',
      analysisBackend,
      '--analysis-max-new-tokens',
      String(analysisMaxNewTokens),
      '--analysis-temperature',
      String(analysisTemperature),
      '--patch-backend',
      patchBackend,
      '--patch-max-new-tokens',
      String(patchMaxNewTokens),
      '--patch-temperature',
      String(patchTemperature)
    ];
    if (analysisBackend !== 'hybrid' && analysisBackend !== 'llm-mock') {
      args.push('--analysis-model', analysisModel || patchModel);
    }
    if (patchBackend !== 'deterministic' && patchBackend !== 'llm-mock') {
      args.push('--patch-model', patchModel);
    }

    const timeoutSeconds = config.get<number>('runtimeTimeoutSeconds', 240);
    return this.runJson(pythonPath, args, repoRoot, workspacePath, timeoutSeconds);
  }

  async checkRuntime(workspace: vscode.WorkspaceFolder): Promise<void> {
    const config = vscode.workspace.getConfiguration('docguard');

    const architecture = config.get<string>('classifierArchitecture', 'staged');
    const inputMode = config.get<string>('modelInputMode', 'raw_diff_plus_docs');

    const repoRoot = path.resolve(this.extensionUri.fsPath, '..');

    const runtimePath = path.join(repoRoot, 'docguard_runtime', 'runtime_cli.py');

    this.output.appendLine('=== DocGuard Runtime Check ===');
    this.output.appendLine(`repoRoot: ${repoRoot}`);
    this.output.appendLine(`workspace: ${workspace.uri.fsPath}`);
    this.output.appendLine(`runtimePath: ${runtimePath}`);
    this.output.appendLine(`architecture: ${architecture}`);

    if (architecture !== 'hybrid_router') {
      const modelPath = path.join(
        repoRoot,
        'models',
        'hf_v0_4',
        inputMode,
        `embedding_classifier${architecture === 'staged' ? '_staged' : ''}.joblib`
      );
      this.output.appendLine(`modelPath: ${modelPath}`);
      try {
        await vscode.workspace.fs.stat(vscode.Uri.file(modelPath));
        this.output.appendLine('classifier model: found');
      } catch {
        this.output.appendLine('classifier model: missing; runtime will use hybrid router fallback');
      }
    }

    await vscode.workspace.fs.stat(vscode.Uri.file(runtimePath));
  }

  private runJson(
    command: string,
    args: string[],
    cwd: string,
    workspacePath: string,
    timeoutSeconds: number
  ): Promise<DocGuardResult> {
    return new Promise((resolve, reject) => {
      const env: NodeJS.ProcessEnv = {
        ...process.env,
        PYTHONPATH: `${cwd}${path.delimiter}${process.env.PYTHONPATH ?? ''}`
      };
      const config = vscode.workspace.getConfiguration('docguard');
      const llmBaseUrl = config.get<string>('llmBaseUrl', '');
      const llmApiKeyEnvVar = config.get<string>('llmApiKeyEnvironmentVariable', 'DOCGUARD_LLM_API_KEY');
      if (llmBaseUrl && !env.DOCGUARD_LLM_BASE_URL) {
        env.DOCGUARD_LLM_BASE_URL = llmBaseUrl;
      }
      if (llmApiKeyEnvVar && process.env[llmApiKeyEnvVar] && !env.DOCGUARD_LLM_API_KEY) {
        env.DOCGUARD_LLM_API_KEY = process.env[llmApiKeyEnvVar];
      }

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

      const timeout = setTimeout(() => {
        child.kill();
      }, Math.max(1, timeoutSeconds) * 1000);

      let stdout = '';
      let stderr = '';

      child.stdout.on('data', chunk => {
        stdout += chunk.toString();
      });

      child.stderr.on('data', chunk => {
        stderr += chunk.toString();
      });

      child.on('error', error => {
        clearTimeout(timeout);
        this.output.appendLine('');
        this.output.appendLine('=== DocGuard Process Error ===');
        this.output.appendLine(String(error));
        reject(error);
      });

      child.on('close', code => {
        clearTimeout(timeout);
        this.output.appendLine('');
        this.output.appendLine('=== DocGuard Runtime Result ===');
        this.output.appendLine(`exit code: ${code}`);
        this.output.appendLine(`stdout: ${stdout}`);
        this.output.appendLine(`stderr: ${stderr}`);

        if (code !== 0) {
          reject(new Error(stderr || stdout || `DocGuard runtime failed with exit code ${code}. It may have timed out while running an LLM backend.`));
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
