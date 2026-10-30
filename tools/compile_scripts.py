#!/usr/bin/env python3
"""Compile all mod scripts using the owner's CPython 2.1 DLL (Windows/MSVC x86)."""
import argparse
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile

from build_pack import PY21_MAGIC, digest_file
from pycompile.shipped_meta import fallback_name, read_meta


def compile_scripts(source, game, output, vcvars=None):
    source, game, output = map(lambda p: Path(p).resolve(), (source, game, output))
    if os.name != "nt":
        raise ValueError("this compiler driver currently supports Windows and MSVC x86")
    if output.exists():
        raise FileExistsError(f"choose a new output directory: {output}")
    scripts = sorted(source.rglob("*.py"))
    if not scripts:
        raise ValueError("no Python sources found")
    if vcvars is None:
        roots = [Path(os.environ.get(n, "C:/Program Files")) for n in ("ProgramFiles", "ProgramFiles(x86)")]
        candidates = [p for root in roots for p in root.glob("Microsoft Visual Studio/*/*/VC/Auxiliary/Build/vcvars32.bat")]
        if not candidates:
            raise ValueError("MSVC x86 tools missing; install C++ build tools or provide --vcvars32")
        vcvars = sorted(set(candidates))[-1]
    vcvars = Path(vcvars).resolve(strict=True)
    if any(c in str(vcvars) for c in '%!\r\n"'):
        raise ValueError("unsupported compiler environment path")
    helper = Path(__file__).parent / "pycompile"
    before = {p.relative_to(source).as_posix(): digest_file(p) for p in scripts}
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="resource-py21-", dir=output.parent) as temporary:
        work = Path(temporary)
        for name in ("vampire_python21.dll", "tier0.dll", "vstdlib.dll"):
            shutil.copy2(game / "Bin" / name, work / name)
        for name in ("py21_host.c", "compile_all.py"):
            shutil.copy2(helper / name, work / name)
        command = work / "build.cmd"
        command.write_text(f'@echo off\ncall "{vcvars}" >nul\nif errorlevel 1 exit /b %errorlevel%\n'
                           'cl /nologo /O1 py21_host.c /Fe:py21_host.exe\n', encoding="utf-8")
        subprocess.run(["cmd", "/c", str(command)], cwd=work, check=True)
        staging = work / "compiled"
        rows = []
        for path in scripts:
            if path.is_symlink() or not path.resolve().is_relative_to(source):
                raise ValueError(f"source symlink refused: {path}")
            relative = path.relative_to(source).as_posix()
            dest = staging / "python" / Path(relative).with_suffix(".pyc")
            dest.parent.mkdir(parents=True, exist_ok=True)
            meta = read_meta(path.with_suffix(".pyc"))
            stamp, name = (struct.unpack("<I", meta[0])[0], meta[1]) if meta else (0, fallback_name(relative))
            if any(c in path.as_posix() + dest.as_posix() for c in "|\r\n"):
                raise ValueError("unsupported source or output path")
            rows.append(f"{path.as_posix()}|{dest.as_posix()}|{stamp}|{name}")
        (work / "targets.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
        subprocess.run([str(work / "py21_host.exe"), "compile_all.py"], cwd=work, check=True)
        log = (work / "compile_log.txt").read_text()
        expected = f"compiled={len(scripts)} failed=0"
        if not log.rstrip().endswith(expected):
            raise ValueError(log)
        if before != {p.relative_to(source).as_posix(): digest_file(p) for p in scripts}:
            raise ValueError("sources changed during compilation")
        for path in staging.rglob("*.pyc"):
            if path.read_bytes()[:4] != PY21_MAGIC:
                raise ValueError(f"not Python 2.1 bytecode: {path}")
        (staging / "compiler-receipt.json").write_text(json.dumps({
            "compiler": "owner-supplied vampire_python21.dll", "pythonMagic": 60202,
            "compilerSha256": digest_file(game / "Bin/vampire_python21.dll"),
            "sources": before, "compiledScripts": len(scripts)}, indent=2) + "\n", encoding="utf-8")
        staging.rename(output)
        return len(scripts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="mod's python directory")
    parser.add_argument("--game", required=True, help="legal Steam/GOG installation with Bin/")
    parser.add_argument("--output", required=True, help="new compiled-output directory")
    parser.add_argument("--vcvars32", help="optional path to MSVC vcvars32.bat")
    args = parser.parse_args()
    count = compile_scripts(args.source, args.game, args.output, args.vcvars32)
    print(f"Compiled all {count} scripts; no source files or game installation modified.")


if __name__ == "__main__":
    main()
