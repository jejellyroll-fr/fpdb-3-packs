#!/usr/bin/env python3
"""Build the stat pack archives from their sources, and refresh every index entry's size and checksum.

    python scripts/build.py           # rebuild and rewrite index.json
    python scripts/build.py --check   # fail if anything is out of date (what CI runs)

A stat pack is kept readable under ``sources/stats/<id>/`` and built into
``stats/<id>.fpdbstats``. The archive is deterministic -- sorted entries, fixed
timestamps and permissions, as fpdb's own export writes it -- so rebuilding an
unchanged pack gives the same bytes and the same checksum.

Standard library only: a contributor needs Python, nothing else.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.json"
SOURCES = ROOT / "sources" / "stats"


def archive(source: Path) -> bytes:
    """The ``.fpdbstats`` archive of the pack folder *source*."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as out:
        for path in sorted(p for p in source.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(path.relative_to(source).as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            out.writestr(info, path.read_bytes())
    return buffer.getvalue()


def build(check: bool) -> list[str]:
    stale: list[str] = []
    for source in sorted(p for p in SOURCES.iterdir() if p.is_dir()):
        target = ROOT / "stats" / f"{source.name}.fpdbstats"
        data = archive(source)
        if not target.is_file() or target.read_bytes() != data:
            stale.append(str(target.relative_to(ROOT)))
            if not check:
                target.write_bytes(data)

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    for entry in index["packs"]:
        package = ROOT / entry["file"]
        if not package.is_file():
            stale.append(f"{entry['id']}: {entry['file']} is missing")
            continue
        data = package.read_bytes()
        digest, size = hashlib.sha256(data).hexdigest(), len(data)
        if (entry.get("sha256"), entry.get("size")) != (digest, size):
            stale.append(f"{entry['id']}: checksum or size in index.json")
            entry["sha256"], entry["size"] = digest, size
    if not check:
        INDEX.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="change nothing; fail if anything is out of date")
    arguments = parser.parse_args()
    stale = build(arguments.check)
    for item in stale:
        print(("out of date: " if arguments.check else "updated: ") + item, file=sys.stderr if arguments.check else sys.stdout)
    if arguments.check and stale:
        print("Run `python scripts/build.py` and commit the result.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
