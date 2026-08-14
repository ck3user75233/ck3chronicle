"""Blind-side P1-PAR-01 runner: execute candidate lexer, know no oracle."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from ck3chronicle.parser import log_blocks as lexical_module


iter_log_blocks = lexical_module.iter_log_blocks


SCHEMA = "ck3chronicle.phase1.lexical-run"
SCHEMA_VERSION = 1


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git(repo: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"candidate Git identity failed ({' '.join(arguments)}): "
            f"{completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def _candidate_identity(repo: Path) -> dict[str, object]:
    repo = repo.resolve()
    top_level = Path(_git(repo, "rev-parse", "--show-toplevel")).resolve()
    if top_level != repo:
        raise RuntimeError(f"--repo is not the candidate Git root: {repo}")
    module_path = Path(lexical_module.__file__).resolve()
    try:
        relative_module = module_path.relative_to(repo).as_posix()
    except ValueError as exc:
        raise RuntimeError(
            f"imported lexer is outside the declared candidate: {module_path}"
        ) from exc
    status = _git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    return {
        "commit": _git(repo, "rev-parse", "HEAD"),
        "tree": _git(repo, "rev-parse", "HEAD^{tree}"),
        "worktree_clean": not bool(status),
        "imported_module": relative_module,
        "imported_module_sha256": _sha256(module_path),
    }


def run(
    error_log: Path,
    *,
    repo: Path,
    require_clean: bool = False,
) -> dict[str, object]:
    candidate = _candidate_identity(repo)
    if require_clean and not candidate["worktree_clean"]:
        raise RuntimeError("release runner requires a clean candidate worktree")
    blocks: list[dict[str, object]] = []
    preamble_blocks = 0
    preamble_bytes = 0
    for block in iter_log_blocks(error_log, log_relpath="error.log"):
        if block.timestamp is None:
            preamble_blocks += 1
            preamble_bytes += block.raw_byte_length
            continue
        blocks.append(
            {
                "index": len(blocks) + 1,
                "start_line": block.line_number,
                "end_line": block.end_line,
                "line_count": block.end_line - block.line_number + 1,
                "timestamp": block.timestamp,
                "level": block.level,
                "source_tag": block.source_tag,
                "source_family": block.source_family,
                "raw_sha256": block.raw_block_sha256,
                "byte_count": block.raw_byte_length,
                "source_block_id": block.source_block_id,
            }
        )
    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "candidate_commit": candidate["commit"],
        "candidate": candidate,
        "input": {
            "relative_role": "error.log",
            "sha256": _sha256(error_log),
            "byte_count": error_log.stat().st_size,
        },
        "summary": {
            "timestamped_block_count": len(blocks),
            "timestamped_block_bytes": sum(
                int(item["byte_count"]) for item in blocks
            ),
            "preamble_block_count": preamble_blocks,
            "preamble_bytes": preamble_bytes,
        },
        "blocks": blocks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--error-log", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Permit a dirty candidate for development calibration only.",
    )
    args = parser.parse_args()
    payload = run(
        args.error_log,
        repo=args.repo,
        require_clean=not args.allow_dirty,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
