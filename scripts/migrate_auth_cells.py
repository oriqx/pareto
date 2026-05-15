"""One-shot rewrite of the auth/connect cell in every pareto notebook.

Three patterns exist today:

A. Starter / submission notebooks
   GATEWAY = os.environ.get("UNIQX_GATEWAY", "localhost:50050")
   API_KEY = os.environ.get("UNIQX_API_KEY")
   client = uniqx.connect(GATEWAY, api_key=API_KEY)

B. Examples that use `endpoint` + `from uniqx import connect`
   endpoint = os.environ.get("UNIQX_GATEWAY", "localhost:50050")
   client = connect(endpoint)

C. Examples that use `GATEWAY_ADDR` + `from uniqx.core.execution import connect`
   GATEWAY_ADDR = os.environ.get("GATEWAY_ADDR", "localhost:50050")
   client = connect(GATEWAY_ADDR, api_key=os.environ.get("UNIQX_API_KEY"))

All become the uniqx.login()-style flow, with the default gateway flipped
to the public hackathon endpoint. The script ensures `login` is in scope
by adding `from uniqx import login` to the cell when it isn't already.

Idempotent. Run with --dry-run to preview.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEARCH_DIRS = ["tracks", "templates", "examples/notebooks"]

DEFAULT_GATEWAY = "api.oriqx.com:443"

# --- Pattern A: starter notebooks ---------------------------------------
A_RE = re.compile(
    r"GATEWAY\s*=\s*os\.environ\.get\([^)]*UNIQX_GATEWAY[^)]*\)[^\n]*\n"
    r"API_KEY\s*=\s*os\.environ\.get\([^)]*UNIQX_API_KEY[^)]*\)[^\n]*\n"
    r"client\s*=\s*uniqx\.connect\(GATEWAY,\s*api_key=API_KEY\)[^\n]*\n",
)
A_NEW = (
    f'GATEWAY = os.environ.get("UNIQX_GATEWAY", "{DEFAULT_GATEWAY}")\n'
    'uniqx.login(os.environ["UNIQX_API_KEY"], gateway=GATEWAY)\n'
    "client = uniqx.connect(GATEWAY)\n"
)

# --- Pattern B: endpoint + bare connect() -------------------------------
B_RE = re.compile(
    r"endpoint\s*=\s*os\.environ\.get\([^)]*UNIQX_GATEWAY[^)]*\)[^\n]*\n"
    r"client\s*=\s*connect\(endpoint\)[^\n]*\n",
)
B_NEW = (
    f'endpoint = os.environ.get("UNIQX_GATEWAY", "{DEFAULT_GATEWAY}")\n'
    'login(os.environ["UNIQX_API_KEY"], gateway=endpoint)\n'
    "client = connect(endpoint)\n"
)
# Drop the now-stale dev-default comment that ships with pattern B.
B_COMMENT_RE = re.compile(
    r"# Default to a local service for development\.\n"
    r"# For prod, export UNIQX_GATEWAY=[^\n]*\n",
)

# --- Pattern C: GATEWAY_ADDR + api_key kwarg ----------------------------
C_RE = re.compile(
    r"GATEWAY_ADDR\s*=\s*os\.environ\.get\([^)]*GATEWAY_ADDR[^)]*\)[^\n]*\n"
    r"client\s*=\s*connect\(\s*GATEWAY_ADDR,\s*api_key=os\.environ\.get\([^)]*UNIQX_API_KEY[^)]*\)\s*\)[^\n]*\n",
)
C_NEW = (
    f'GATEWAY_ADDR = os.environ.get("GATEWAY_ADDR", "{DEFAULT_GATEWAY}")\n'
    'login(os.environ["UNIQX_API_KEY"], gateway=GATEWAY_ADDR)\n'
    "client = connect(GATEWAY_ADDR)\n"
)

# Pre-existing imports we extend rather than duplicate.
FROM_UNIQX_IMPORT_RE = re.compile(
    r"(from uniqx import (?:[^\n]+))",
)


def _ensure_login_in_scope(source: str, pattern: str) -> str:
    """Ensure `login` is callable in the cell. Pattern A uses ``uniqx.login``
    (the module is already imported as ``uniqx``); B/C use bare ``login``."""
    if pattern == "A":
        return source  # uniqx.login uses the existing `import uniqx`
    if "login(" not in source:
        # Defensive — should not hit since we just inserted login(...) above.
        return source
    # If the cell has `from uniqx import …` already, extend it.
    m = FROM_UNIQX_IMPORT_RE.search(source)
    if m:
        existing = m.group(1)
        if re.search(r"\blogin\b", existing):
            return source  # already imports login
        # Extend the existing import.
        new_import = existing.rstrip() + ", login"
        return source.replace(existing, new_import, 1)
    # Otherwise prepend a fresh import after the os import (so ruff stays
    # happy: stdlib first, then third party).
    lines = source.splitlines(keepends=True)
    insert_at = 0
    for idx, ln in enumerate(lines):
        if ln.startswith("import ") or ln.startswith("from "):
            insert_at = idx + 1
    lines.insert(insert_at, "from uniqx import login\n")
    return "".join(lines)


def rewrite_source(source: str) -> tuple[str, str] | None:
    if "uniqx.login(" in source or "login(os.environ" in source:
        return None
    for label, regex, replacement in (
        ("A", A_RE, A_NEW),
        ("B", B_RE, B_NEW),
        ("C", C_RE, C_NEW),
    ):
        new, n = regex.subn(replacement, source, count=1)
        if n == 1:
            if label == "B":
                new = B_COMMENT_RE.sub("", new, count=1)
            new = _ensure_login_in_scope(new, label)
            return new, label
    return None


def iter_notebooks() -> list[Path]:
    paths: list[Path] = []
    for d in SEARCH_DIRS:
        paths.extend((ROOT / d).rglob("*.ipynb"))
    return sorted(paths)


def _detect_ascii_only(raw: str) -> bool:
    """True if the on-disk file already encodes non-ASCII as \\uXXXX.

    We sniff a small sample. Mixed files lean ASCII-escaped (the common
    nbformat style), so default to True on a tie.
    """
    sample = raw[:8192]
    return all(ord(c) < 128 for c in sample)


def process(path: Path, dry_run: bool) -> str:
    raw = path.read_text(encoding="utf-8")
    ascii_only = _detect_ascii_only(raw)
    trailing_newline = raw.endswith("\n")
    nb = json.loads(raw)
    cells = nb.get("cells", [])
    for cell in cells:
        if cell.get("cell_type") != "code":
            continue
        src = "".join(cell.get("source", []))
        if "connect(" not in src:
            continue
        if "UNIQX_GATEWAY" not in src and "GATEWAY_ADDR" not in src:
            continue
        if "uniqx.login(" in src or "login(os.environ" in src:
            return "skipped-already-login"
        result = rewrite_source(src)
        if result is None:
            return "skipped-no-match"
        new_src, label = result
        if not dry_run:
            original = cell.get("source", "")
            if isinstance(original, list):
                cell["source"] = new_src.splitlines(keepends=True)
            else:
                cell["source"] = new_src
            # Match the original file's encoding choice so the diff stays
            # scoped to the cell we touched (no spurious unicode churn
            # in unrelated markdown cells).
            out = json.dumps(nb, indent=1, ensure_ascii=ascii_only)
            if trailing_newline:
                out += "\n"
            path.write_text(out, encoding="utf-8")
        return f"rewrote-{label}"
    return "skipped-no-match"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    counts: dict[str, int] = {}
    no_match: list[Path] = []
    for nb_path in iter_notebooks():
        outcome = process(nb_path, args.dry_run)
        counts[outcome] = counts.get(outcome, 0) + 1
        rel = nb_path.relative_to(ROOT)
        if outcome.startswith("rewrote"):
            print(f"[{'DRY' if args.dry_run else 'WROTE'}] [{outcome[-1]}] {rel}")
        elif outcome == "skipped-no-match":
            no_match.append(rel)

    print()
    print("Summary:")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    if no_match:
        print()
        print("Notebooks with no matching auth cell (review manually):")
        for p in no_match:
            print(f"  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
