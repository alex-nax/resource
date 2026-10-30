#!/usr/bin/env python3
"""Build or verify a local Unofficial Patch distribution pack (Python 3.9+)."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import struct
import zipfile

PY21_MAGIC = struct.pack("<H", 60202) + b"\r\n"
AUTHOR = "Werner Spahl (Wesp5)"
UP_PREFIX = "vtmb/Unofficial_Patch/"
PYC_PREFIX = UP_PREFIX + "python/"
EXCLUDED_DIRS = {"save", "saves", "profiles", "screenshots", "logs", "crashes", "dlls", "cl_dlls", "bin"}
EXCLUDED_NAMES = {"config.cfg", "settings.cfg", "autoexec-personal.cfg", "thumbs.db", "desktop.ini"}
NATIVE_SUFFIXES = {".exe", ".dll", ".asi", ".so", ".dylib", ".vtm"}


def excluded(path):
    parts = PurePosixPath(path).parts
    return (any(p.startswith(".") or p.lower() in EXCLUDED_DIRS for p in parts)
            or parts[-1].lower() in EXCLUDED_NAMES
            or PurePosixPath(path).suffix.lower() in NATIVE_SUFFIXES)


def files_under(root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError(f"not a directory: {root}")
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
            raise ValueError(f"symlink/junction is not packable: {path}")
        if not path.resolve().is_relative_to(root):
            raise ValueError(f"path escapes source: {path}")
        if path.is_file():
            yield path.relative_to(root).as_posix(), path


def digest_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def check_bytecode(path):
    with path.open("rb") as stream:
        header = stream.read(9)
    if len(header) < 9 or header[:4] != PY21_MAGIC or header[8:9] != b"c":
        raise ValueError(f"not CPython 2.1 code bytecode: {path}")


def allowed_member(name):
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name:
        return False
    if name in {"vtmb/credits/VTMBup-readme.txt", "vtmb/credits/compiler-receipt.json"}:
        return True
    if name.startswith(UP_PREFIX):
        return not excluded(name[len(UP_PREFIX):])
    return name.startswith(PYC_PREFIX) and name.endswith(".pyc") and not excluded(name[len(PYC_PREFIX):])


def verify(archive_path):
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("duplicate archive paths")
        if "vtmb/pack.json" not in names or any(n != "vtmb/pack.json" and not allowed_member(n) for n in names):
            raise ValueError("unexpected or unsafe archive path")
        manifest = json.loads(archive.read("vtmb/pack.json"))
        if manifest.get("schemaVersion") != 1 or manifest.get("id") != "unofficial-patch":
            raise ValueError("unsupported pack manifest")
        if manifest.get("author") != AUTHOR:
            raise ValueError("missing Wesp5 attribution")
        rows = manifest["files"]
        declared = {row["path"] for row in rows}
        if len(declared) != len(rows) or set(names) != declared | {"vtmb/pack.json"}:
            raise ValueError("unexpected or undeclared file")
        sources, compiled = set(), set()
        for row in rows:
            name = row["path"]
            digest = hashlib.sha256()
            size = 0
            header = b""
            with archive.open(name) as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    if not header:
                        header = block[:9]
                    size += len(block)
                    digest.update(block)
            if size != row["bytes"] or digest.hexdigest() != row["sha256"]:
                raise ValueError(f"size/hash mismatch: {name}")
            if name.startswith(UP_PREFIX + "python/") and name.endswith(".py"):
                sources.add(name[len(UP_PREFIX + "python/"):-3])
            if name.startswith(PYC_PREFIX) and name.endswith(".pyc"):
                if header[:4] != PY21_MAGIC or header[8:9] != b"c":
                    raise ValueError(f"not CPython 2.1 code bytecode: {name}")
                compiled.add(name[len(PYC_PREFIX):-4])
        if not sources or sources != compiled or len(compiled) != manifest.get("compiledScripts"):
            raise ValueError("missing or extra compiled scripts")
        receipt = json.loads(archive.read("vtmb/credits/compiler-receipt.json"))
        source_hashes = {row["path"][len(UP_PREFIX + "python/"):]: row["sha256"] for row in rows
                         if row["path"].startswith(UP_PREFIX + "python/") and row["path"].endswith(".py")}
        if receipt.get("sources") != source_hashes or receipt.get("pythonMagic") != 60202:
            raise ValueError("stale compiler receipt: sources changed")
        if b"Wesp5" not in archive.read("vtmb/credits/VTMBup-readme.txt"):
            raise ValueError("Wesp5 original credits required")
        return manifest


def build(source, compiled_root, readme, output, version):
    source, compiled_root, readme, output = map(Path, (source, compiled_root, readme, output))
    if output.exists():
        raise FileExistsError(output)
    if source.name.lower() == "vampire":
        raise ValueError("base game files are not a patch pack")
    if b"Wesp5" not in readme.read_bytes():
        raise ValueError("the original Wesp5 readme is required")
    entries = [(UP_PREFIX + rel, path) for rel, path in files_under(source)
               if not excluded(rel) and not (rel.startswith("python/") and rel.endswith(".pyc"))]
    sources = {name[len(UP_PREFIX + "python/"):-3] for name, _ in entries
               if name.startswith(UP_PREFIX + "python/") and name.endswith(".py")}
    compiled = {rel[:-4]: path for rel, path in files_under(compiled_root / "python") if rel.endswith(".pyc")}
    if not sources or sources != set(compiled):
        raise ValueError(f"missing compiled scripts: {sorted(sources - set(compiled))}; "
                         f"extra compiled scripts: {sorted(set(compiled) - sources)}")
    for name, path in compiled.items():
        check_bytecode(path)
        entries.append((PYC_PREFIX + name + ".pyc", path))
    receipt_path = compiled_root / "compiler-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    hashes = {name[len(UP_PREFIX + "python/"):]: digest_file(path) for name, path in entries
              if name.startswith(UP_PREFIX + "python/") and name.endswith(".py")}
    if receipt.get("sources") != hashes or receipt.get("pythonMagic") != 60202:
        raise ValueError("stale compiler receipt: sources changed; recompile")
    entries.append(("vtmb/credits/compiler-receipt.json", receipt_path))
    entries.append(("vtmb/credits/VTMBup-readme.txt", readme))
    entries.sort()
    manifest = {"schemaVersion": 1, "id": "unofficial-patch", "version": version,
                "name": "Unofficial Patch", "author": AUTHOR,
                "homepage": "https://www.moddb.com/mods/vtmb-unofficial-patch",
                "requires": {"game": "Vampire: The Masquerade - Bloodlines", "legalCopy": True,
                             "stores": ["Steam", "GOG"]},
                "compiledScripts": len(compiled), "pythonMagic": 60202,
                "files": [{"path": name, "bytes": path.stat().st_size, "sha256": digest_file(path)}
                          for name, path in entries]}
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".partial")
    with zipfile.ZipFile(temporary, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, path in entries:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            with path.open("rb") as src, archive.open(info, "w", force_zip64=True) as dest:
                shutil.copyfileobj(src, dest, 1024 * 1024)
        archive.writestr("vtmb/pack.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    verify(temporary)
    with temporary.open("rb") as src, output.open("xb") as dest:
        shutil.copyfileobj(src, dest, 1024 * 1024)
    temporary.unlink()
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    make = commands.add_parser("build")
    for name in ("source", "compiled", "readme", "output", "version"):
        make.add_argument("--" + name, required=True)
    check = commands.add_parser("verify")
    check.add_argument("archive", type=Path)
    args = parser.parse_args()
    if args.command == "verify":
        result = verify(args.archive)
        output = args.archive
    else:
        result = build(args.source, args.compiled, args.readme, args.output, args.version)
        output = Path(args.output)
    print(json.dumps({"archive": str(output), "sha256": digest_file(output), "version": result["version"],
                      "files": len(result["files"]), "compiledScripts": result["compiledScripts"]}, indent=2))


if __name__ == "__main__":
    main()
