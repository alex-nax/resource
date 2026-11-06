#!/usr/bin/env python3
"""Build the Unofficial Patch's Plus overlay from an unpacked installer (Python 3.9+).

Spec: docs/specs/maintenance-2026-11-05-patch-variants.md. Unpack with `innoextract --collisions rename`.
Names no files: the installer's tags and the base tree decide. Writes only under --out.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

REFUSED_DIRS = {"python", "maps"}


def digest(path):
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def files_under(root):
    return {path.relative_to(root).as_posix(): path for path in sorted(root.rglob("*")) if path.is_file()}


def plan_overlay(installer, base):
    """rel-path -> source file, and a report. Refuses a Python file or a map: see the spec."""
    installer, base = Path(installer), Path(base)
    found = files_under(installer)
    base_files = {rel.lower(): path for rel, path in files_under(base).items()}
    variants = {}
    plain = {}
    for rel, path in found.items():
        stem, tag = rel.rsplit("#", 1) if "#" in rel.rsplit("/", 1)[-1] else (rel, "")
        if tag:
            variants.setdefault(stem, {})[tag] = path
        else:
            plain[rel] = path
    # The installer overwrites by name on a case-insensitive disk: `LightningBird.mdl` is `lightningbird.mdl#basic`'s twin.
    plain_folded = {rel.lower(): path for rel, path in plain.items()}
    variant_folded = {stem.lower() for stem in variants}
    overlay, report = {}, {"pairs": 0, "identicalToBase": [], "conflicts": [], "added": 0}
    for stem, tags in variants.items():
        if "basic" not in tags:
            continue
        plus = tags.get("plus") or plain.get(stem) or plain_folded.get(stem.lower())
        if plus is None:
            continue
        report["pairs"] += 1
        on_base = base_files.get(stem.lower())
        if on_base is not None and digest(plus) == digest(on_base):
            report["identicalToBase"].append(stem)
            continue
        if on_base is not None and digest(tags["basic"]) != digest(on_base):
            report["conflicts"].append(stem)
        overlay[stem] = plus
    for rel, path in plain.items():
        if rel.lower() not in variant_folded and rel.lower() not in base_files:
            overlay[rel] = path
            report["added"] += 1
    refused = sorted(rel for rel in overlay if rel.split("/")[0].lower() in REFUSED_DIRS)
    if refused:
        raise ValueError(f"the overlay may not change scripts or maps: {refused[:10]}")
    report["conflicts"].sort()
    report["identicalToBase"].sort()
    report["files"] = len(overlay)
    report["bytes"] = sum(path.stat().st_size for path in overlay.values())
    return overlay, report


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--installer", type=Path, required=True, help="the unpacked installer's Unofficial_Patch")
    parser.add_argument("--base", type=Path, required=True, help="the Basic tree the pack ships")
    parser.add_argument("--out", type=Path, required=True, help="a new directory for the overlay")
    args = parser.parse_args()
    if args.out.exists():
        print(f"choose a new output directory: {args.out}", file=sys.stderr)
        return 2
    overlay, report = plan_overlay(args.installer, args.base)
    for rel, source in overlay.items():
        target = args.out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
