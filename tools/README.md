# Pack maintainer tools

These tools are for pack maintainers, not player installation. Players use
[SideQuest and the ready-to-use pack](../instructions.md); no Python or compilation
is required. Maintainers need Python 3.9+ for the tools below.

## Verify or build the Unofficial Patch pack

`build_pack.py verify PACK.zip` checks every declared file hash and script coverage.
The build command takes an installed patch, a fresh compiler result, and the
original Wesp5 readme. It excludes personal saves/configuration and native programs,
refuses stale/missing bytecode and never overwrites an existing output.

```text
python tools/build_pack.py build --source "C:/Bloodlines/Unofficial_Patch" --compiled "C:/ReSource/compiled" --readme "C:/Bloodlines/VTMBup-readme.txt" --version YOUR-PACK-VERSION --output "C:/ReSource/patch.zip"
```

## Compile all scripts

On Windows, install Visual Studio C++ build tools with x86 support. The compiler
uses the Python 2.1 DLLs in **your legal game installation**; no proprietary DLLs
are shipped here. It compiles every `.py` in the source tree and writes a freshness
receipt. Choose a new output directory on each run.

```text
python tools/compile_scripts.py --source "C:/Bloodlines/Unofficial_Patch/python" --game "C:/Bloodlines" --output "C:/ReSource/compiled"
```

`--vcvars32` can name a specific Visual Studio `vcvars32.bat`. The compiler driver
currently supports Windows; Wine/macOS/Linux wrapping is not advertised yet.
The small `pycompile/` helpers are ReSource build tools, not game script sources.

## Developer deployment helper

`quest_deploy.py` remains available for development automation. It is not part of
the player installation procedure. Players copy the single `vtmb` folder using
SideQuest, following [the installation instructions](../instructions.md).

## OpenAL relinking

`relink_openal.py` consumes the object files and recipe from the matching release's
OpenAL source/relink archive. Follow the archive's README to rebuild the library
and relink a modified APK. This is optional developer tooling, not a player step.
