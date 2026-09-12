from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Callable, Iterable


PROVENANCE_RE = re.compile(
    r"^<!--\s*(?P<path>.+?)\s+@\s+(?P<ref>[0-9a-f]{40}|controlled-baseline:[0-9a-f]{16})\s*-->",
    re.IGNORECASE,
)
DOC_EXTENSIONS = {".md", ".mdx", ".rst"}
TXT_DOC_HINTS = {"readme", "documentation", "docs", "guide", "manual", "api", "configuration", "setup", "usage"}
EXCLUDED_PARTS = {"node_modules", "vendor", "dist", "build", "coverage", ".next", "generated", "gen", "out"}
HISTORY_NAMES = {"changelog", "changes", "history", "releases", "news"}


@dataclass(frozen=True)
class PreChangeSource:
    kind: str
    repository: str
    revision: str
    local_root: str | None = None
    provenance_path: str | None = None


@dataclass(frozen=True)
class DocumentCandidate:
    path: str
    headings: tuple[str, ...]
    content: str
    priority_tier: str
    path_distance: int
    identifier_overlap: int


@dataclass(frozen=True)
class DocumentChunk:
    path: str
    heading: str
    heading_path: tuple[str, ...]
    text: str
    chunk_index: int
    priority_tier: str = ""
    path_distance: int = 0
    identifier_overlap: int = 0


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_pre_change_marker(docs_before_excerpt: str) -> tuple[str, str] | None:
    match = PROVENANCE_RE.match(str(docs_before_excerpt or ""))
    if not match:
        return None
    return match.group("path").replace("\\", "/"), match.group("ref").lower()


def resolve_pre_change_source(row: dict, *, root: Path) -> PreChangeSource:
    marker = parse_pre_change_marker(str(row.get("docs_before_excerpt") or ""))
    if marker is None:
        raise ValueError(f"{row.get('case_id')}: missing explicit pre-change provenance marker")
    marker_path, revision = marker
    repository = str(row.get("repository") or "").strip()
    if re.fullmatch(r"[0-9a-f]{40}", revision):
        if repository.count("/") != 1 or repository.lower().startswith("controlled"):
            raise ValueError(f"{row.get('case_id')}: natural Git source requires owner/repository")
        return PreChangeSource("git_commit", repository, revision, provenance_path=marker_path)
    source_dataset = str(row.get("source_dataset") or row.get("consolidated_source_dataset") or "").strip()
    source_copy = str(row.get("source_copy_path") or "").strip()
    if not source_dataset or not source_copy:
        raise ValueError(f"{row.get('case_id')}: controlled baseline lacks source-copy metadata")
    local_root = (root / "data/final_v2" / source_dataset / source_copy).resolve()
    allowed = (root / "data/final_v2").resolve()
    if allowed not in local_root.parents or not local_root.is_dir():
        raise ValueError(f"{row.get('case_id')}: invalid controlled baseline root")
    return PreChangeSource("frozen_controlled_baseline", repository, revision, str(local_root), marker_path)


def assert_explicit_commit(revision: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", str(revision or "").lower()):
        raise ValueError("Repository access requires an explicit 40-hex pre-change commit; HEAD/branches are forbidden")


class BareGitRepositoryProvider:
    """Read trees/blobs only from explicit pre-change commits in a bare cache."""

    def __init__(self, cache_root: Path, *, runner: Callable[..., subprocess.CompletedProcess] = subprocess.run):
        self.cache_root = cache_root
        self.runner = runner

    def cache_path(self, repository: str) -> Path:
        safe = repository.replace("/", "__")
        return self.cache_root / f"{safe}.git"

    def _run(self, args: list[str], *, cwd: Path | None = None, capture: bool = True) -> subprocess.CompletedProcess:
        return self.runner(args, cwd=cwd, check=True, text=True, encoding="utf-8", errors="replace", capture_output=capture)

    def ensure_repository(self, repository: str) -> Path:
        cache = self.cache_path(repository)
        if not (cache / "config").is_file():
            cache.parent.mkdir(parents=True, exist_ok=True)
            self._run(["git", "init", "--bare", str(cache)])
            self._run(["git", "remote", "add", "origin", f"https://github.com/{repository}.git"], cwd=cache)
        return cache

    def ensure_commits(self, repository: str, revisions: Iterable[str]) -> dict[str, bool]:
        revisions = sorted(set(str(item).lower() for item in revisions))
        for revision in revisions:
            assert_explicit_commit(revision)
        cache = self.ensure_repository(repository)
        result: dict[str, bool] = {}
        missing: list[str] = []
        for revision in revisions:
            probe = subprocess.run(["git", "cat-file", "-e", f"{revision}^{{commit}}"], cwd=cache, capture_output=True)
            if probe.returncode == 0:
                result[revision] = True
            else:
                missing.append(revision)
        if missing:
            try:
                self._run(
                    ["git", "-c", "protocol.version=2", "fetch", "--no-tags", "--depth=1", "--filter=blob:none", "origin", *missing],
                    cwd=cache,
                )
            except subprocess.CalledProcessError:
                # Isolate an unavailable SHA without losing other explicit commits.
                # Never fall back to HEAD or a branch.
                for revision in missing:
                    try:
                        self._run(
                            ["git", "-c", "protocol.version=2", "fetch", "--no-tags", "--depth=1", "--filter=blob:none", "origin", revision],
                            cwd=cache,
                        )
                    except subprocess.CalledProcessError:
                        pass
        for revision in missing:
            probe = subprocess.run(["git", "cat-file", "-e", f"{revision}^{{commit}}"], cwd=cache, capture_output=True)
            result[revision] = probe.returncode == 0
        return result

    def list_paths(self, repository: str, revision: str) -> list[str]:
        assert_explicit_commit(revision)
        cache = self.cache_path(repository)
        completed = self._run(["git", "ls-tree", "-r", "--name-only", revision], cwd=cache)
        return [line.strip().replace("\\", "/") for line in completed.stdout.splitlines() if line.strip()]

    def read_text(self, repository: str, revision: str, relative_path: str, *, max_bytes: int = 2_000_000) -> str:
        assert_explicit_commit(revision)
        normalized = PurePosixPath(relative_path).as_posix()
        if normalized.startswith("../") or normalized.startswith("/"):
            raise ValueError("Document path escapes repository")
        cache = self.cache_path(repository)
        completed = subprocess.run(["git", "show", f"{revision}:{normalized}"], cwd=cache, check=True, capture_output=True)
        if len(completed.stdout) > max_bytes:
            raise ValueError(f"Document exceeds {max_bytes} bytes: {normalized}")
        return completed.stdout.decode("utf-8", errors="replace")


def is_documentation_path(path: str, *, allow_history: bool = False) -> bool:
    normalized = PurePosixPath(path.replace("\\", "/"))
    parts = [part.casefold() for part in normalized.parts]
    if any(part in EXCLUDED_PARTS for part in parts):
        return False
    stem = normalized.stem.casefold()
    if not allow_history and stem in HISTORY_NAMES:
        return False
    suffix = normalized.suffix.casefold()
    if suffix in DOC_EXTENSIONS:
        return True
    if suffix == ".txt":
        return any(hint in stem for hint in TXT_DOC_HINTS) or any(part in {"docs", "documentation"} for part in parts)
    return False


def path_distance(document_path: str, changed_paths: list[str]) -> int:
    doc_parts = PurePosixPath(document_path).parent.parts
    best = 10_000
    for changed in changed_paths:
        changed_parts = PurePosixPath(changed.replace("\\", "/")).parent.parts
        common = 0
        for left, right in zip(doc_parts, changed_parts):
            if left.casefold() != right.casefold():
                break
            common += 1
        best = min(best, len(doc_parts) + len(changed_parts) - 2 * common)
    return best if best < 10_000 else len(doc_parts)


def candidate_priority(path: str, changed_paths: list[str]) -> str:
    normalized = PurePosixPath(path)
    lower_parts = [part.casefold() for part in normalized.parts]
    name = normalized.name.casefold()
    doc_parent = normalized.parent.as_posix().casefold().strip(".")
    for changed in changed_paths:
        parent = PurePosixPath(changed.replace("\\", "/")).parent.as_posix().casefold().strip(".")
        if name.startswith("readme") and (doc_parent == parent or (doc_parent and parent.startswith(doc_parent + "/"))):
            return "A"
    if any(part in {"docs", "documentation"} for part in lower_parts) or "/website/docs/" in f"/{normalized.as_posix().casefold()}/":
        return "B"
    if len(normalized.parts) == 1 and any(name.startswith(prefix) for prefix in ("readme", "contributing", "migration", "configuration", "api")):
        return "C"
    if name.startswith("readme") and any(part in {"packages", "examples"} for part in lower_parts):
        return "B"
    return "D"


def extract_identifiers(code_diff: str) -> list[str]:
    tokens = re.findall(r"\b[A-Za-z_][A-Za-z0-9_.-]{2,}\b", str(code_diff or ""))
    stop = {"diff", "git", "index", "return", "const", "function", "class", "true", "false", "string", "number"}
    return sorted({token for token in tokens if token.casefold() not in stop}, key=lambda value: (value.casefold(), value))


def extract_headings(text: str) -> tuple[str, ...]:
    headings: list[str] = []
    lines = str(text or "").splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            headings.append(match.group(1).strip())
        elif index + 1 < len(lines) and re.match(r"^\s*(?:=+|-+)\s*$", lines[index + 1]) and line.strip():
            headings.append(line.strip())
    return tuple(headings)


def discover_candidates(paths: Iterable[str], *, changed_paths: list[str], code_diff: str) -> list[tuple[str, str, int, int]]:
    identifiers = [item.casefold() for item in extract_identifiers(code_diff)]
    allow_history = any(PurePosixPath(path).stem.casefold() in HISTORY_NAMES for path in changed_paths)
    candidates = []
    for path in sorted(set(item.replace("\\", "/") for item in paths), key=lambda value: (value.casefold(), value)):
        if not is_documentation_path(path, allow_history=allow_history):
            continue
        overlap = sum(1 for identifier in identifiers if identifier in path.casefold())
        candidates.append((path, candidate_priority(path, changed_paths), path_distance(path, changed_paths), overlap))
    return sorted(candidates, key=lambda item: (item[1], item[2], -item[3], item[0].casefold(), item[0]))


def semantic_chunks(
    path: str,
    text: str,
    *,
    max_chars: int = 4000,
    priority_tier: str = "",
    distance: int = 0,
    identifier_overlap: int = 0,
) -> list[DocumentChunk]:
    lines = str(text or "").splitlines()
    sections: list[tuple[tuple[str, ...], list[str]]] = []
    heading_stack: list[str] = []
    current: list[str] = []
    current_path: tuple[str, ...] = ()

    def flush() -> None:
        nonlocal current
        body = "\n".join(current).strip()
        if body:
            sections.append((current_path, current))
        current = []

    for index, line in enumerate(lines):
        match = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if match:
            flush()
            level = len(match.group(1))
            heading_stack[:] = heading_stack[: level - 1]
            heading_stack.append(match.group(2).strip())
            current_path = tuple(heading_stack)
        current.append(line)
    flush()
    if not sections and str(text or "").strip():
        sections = [((), str(text).splitlines())]

    output: list[DocumentChunk] = []
    chunk_index = 0
    for heading_path, section_lines in sections:
        buffer: list[str] = []
        length = 0
        for line in section_lines:
            added = len(line) + 1
            if buffer and length + added > max_chars:
                output.append(DocumentChunk(path, heading_path[-1] if heading_path else "", heading_path, "\n".join(buffer).strip(), chunk_index, priority_tier, distance, identifier_overlap))
                chunk_index += 1
                buffer = []
                length = 0
            buffer.append(line)
            length += added
        if buffer:
            output.append(DocumentChunk(path, heading_path[-1] if heading_path else "", heading_path, "\n".join(buffer).strip(), chunk_index, priority_tier, distance, identifier_overlap))
            chunk_index += 1
    return output


def source_receipt(source: PreChangeSource) -> dict:
    payload = asdict(source)
    payload["pre_change_enforced"] = True
    payload["head_access_allowed"] = False
    return payload
