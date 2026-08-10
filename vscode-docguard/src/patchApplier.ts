import * as vscode from 'vscode';
import { DocGuardPatch } from './types';

export async function applyPatch(workspace: vscode.WorkspaceFolder, patch: DocGuardPatch): Promise<void> {
  const uri = vscode.Uri.joinPath(workspace.uri, patch.file);
  let content = '';
  try {
    content = Buffer.from(await vscode.workspace.fs.readFile(uri)).toString('utf8');
  } catch {
    const initial = `# ${patch.section}\n\n${patch.text}\n`;
    await vscode.workspace.fs.writeFile(uri, Buffer.from(initial, 'utf8'));
    const doc = await vscode.workspace.openTextDocument(uri);
    await doc.save();
    return;
  }
  const heading = new RegExp(`^#{1,6}\\s+${escapeRegExp(patch.section)}\\s*$`, 'm');
  const match = content.match(heading);
  let next = content;
  if (!match || match.index === undefined) {
    next = `${content.trimEnd()}\n\n## ${patch.section}\n\n${patch.text}\n`;
  } else {
    const start = match.index + match[0].length;
    const rest = content.slice(start);
    const nextHeading = rest.search(/^#{1,6}\s+/m);
    const insertAt = nextHeading < 0 ? content.length : start + nextHeading;
    next = `${content.slice(0, insertAt).trimEnd()}\n${patch.text}\n\n${content.slice(insertAt).trimStart()}`;
  }
  const edit = new vscode.WorkspaceEdit();
  edit.replace(uri, new vscode.Range(0, 0, Number.MAX_SAFE_INTEGER, 0), next);
  await vscode.workspace.applyEdit(edit);
  const doc = await vscode.workspace.openTextDocument(uri);
  await doc.save();
}

function escapeRegExp(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

