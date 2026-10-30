#!/usr/bin/env python3
"""Relink a release's supplied object files against an OpenAL static library."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kit", type=Path, required=True)
    parser.add_argument("--ndk", type=Path, required=True)
    parser.add_argument("--openal", type=Path, help="replacement libopenal.a; defaults to the supplied original")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    kit = args.kit.resolve()
    ndk = args.ndk.resolve()
    recipe = json.loads((kit / "recipe.json").read_text(encoding="utf-8"))
    properties = (ndk / "source.properties").read_text(encoding="utf-8")
    if recipe["ndkVersion"] not in properties:
        parser.error("Use the NDK version specified in recipe.json")
    host = "windows-x86_64" if os.name == "nt" else ("darwin-x86_64" if os.uname().sysname == "Darwin" else "linux-x86_64")
    compiler = ndk / "toolchains/llvm/prebuilt" / host / "bin" / ("clang++.exe" if os.name == "nt" else "clang++")
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    openal = args.openal.resolve() if args.openal else kit / recipe["originalOpenal"]
    substitutions = {"${ROOT}": kit.as_posix(), "${NDK}": ndk.as_posix(),
                     "${HOST}": host, "${OUTPUT}": output.as_posix(), "${OPENAL}": openal.as_posix()}
    command = []
    for argument in recipe["arguments"]:
        for key, value in substitutions.items():
            argument = argument.replace(key, value)
        command.append(argument)
    with tempfile.TemporaryDirectory(prefix="relink-") as temporary:
        response = Path(temporary) / "link.rsp"
        response.write_text("\n".join('"' + item.replace('"', '\\"') + '"' for item in command), encoding="utf-8")
        subprocess.run([str(compiler), "@" + str(response)], check=True)
    print("Relinked library:", output)


if __name__ == "__main__":
    main()
