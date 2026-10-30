#!/usr/bin/env python3
"""F943 — the two header/marshal fields a .pyc carries that are not the bytecode.

Byte-identity with the game's own output needs both, and neither can be reconstructed by rule:

  * co_filename — vanilla's strings mix separators irregularly ("python\\fileutil.py" but
    "python/theatre\\theatre.py"), so the only correct value is the one in the shipped file.
  * mtime — the 4 bytes after the magic. Our driver wrote zeros.

For a source with no shipped .pyc (the campaign hubs) there is nothing to copy, so the caller
supplies vanilla's SHAPE without a machine prefix — decision 5 in
docs/specs/feature-943-campaign-hubs.md. This module only reports what is there.
"""
import re
import struct
import sys
from pathlib import Path


def read_meta(pyc: Path):
    """(mtime_bytes, co_filename) from a shipped 2.1 .pyc, or None if it has neither."""
    try:
        blob = pyc.read_bytes()
    except OSError:
        return None
    if len(blob) < 9:
        return None
    mtime = blob[4:8]
    # marshal string: 's' + int32 length + bytes. co_filename is interned once and is the first
    # printable run ending in .py
    for m in re.finditer(rb"s(....)", blob, re.S):
        n = struct.unpack("<i", m.group(1))[0]
        if 0 < n < 300:
            s = blob[m.end():m.end() + n]
            if s.endswith(b".py") and all(32 <= c < 127 for c in s):
                return mtime, s.decode("latin-1")
    return None


def fallback_name(rel: str) -> str:
    """Vanilla's shape for a module it never shipped compiled, with no invented machine prefix.

    Its own subdirectory modules read `python/<dir>\\<file>.py` (theatre, tutorial), so a hub
    follows that.
    """
    parts = rel.split("/")
    if len(parts) > 1:
        return "Unofficial_Patch/python/" + "/".join(parts[:-1]) + "\\" + parts[-1]
    return "Unofficial_Patch/python\\" + parts[-1]


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: shipped_meta.py <source-root> <relative/path.py>", file=sys.stderr)
        return 2
    root, rel = Path(sys.argv[1]), sys.argv[2]
    meta = read_meta(root / (rel[:-3] + ".pyc"))
    if meta is None:
        print("0|" + fallback_name(rel))
    else:
        mtime, name = meta
        print(str(struct.unpack("<I", mtime)[0]) + "|" + name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
