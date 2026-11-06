# Pack maintainer tools

These tools are for pack maintainers, not player installation. Players use
[SideQuest and the ready-to-use pack](../instructions.md); no Python or compilation
is required. Maintainers need Python 3.9+ for the tools below.

## Verify or build the Unofficial Patch pack

`build_pack.py verify PACK.zip` checks every declared file hash and script coverage.
Run `prepare_variants.py` first on the patch installer unpacked with `innoextract --collisions rename`: it writes the
Plus overlay that `--plus-variant` takes. The build command takes an installed patch, a fresh compiler result, the
original Wesp5 readme, and `--game` plus `--extractor` (`vtmb-modconv`), which extract the data the port
needs from the patch's DLLs. It excludes personal saves/configuration and native programs, DLLs included,
refuses stale/missing bytecode and never overwrites an existing output.
Supply the patch installer's `Vampire/scripts/liblist.gam` with `--game-info` if
the overlay lacks it. Both configured launch maps must exist in the patch.

```text
python tools/build_pack.py build --source "C:/Bloodlines/Unofficial_Patch" --compiled "C:/ReSource/compiled" --readme "C:/Bloodlines/VTMBup-readme.txt" --game-info "C:/Bloodlines/Vampire/scripts/liblist.gam" --version YOUR-PACK-VERSION --output "C:/ReSource/patch.zip"
```

To make the small 0.1.0 startup fix (extracted directly into `vtmb`):

```text
python tools/build_pack.py game-info-fix --source "C:/Bloodlines/Unofficial_Patch" --game-info "C:/Bloodlines/Vampire/scripts/liblist.gam" --output "C:/ReSource/vtmb-new-game-fix-0.1.0.zip"
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

## OpenAL source and legacy relinking

`relink_openal.py` is for the historical 0.1.0 source/relink archive.
Releases from 0.1.1 dynamically link OpenAL and provide its source and rebuild
recipe instead; they do not need this tool. Follow the archive's README to rebuild the library,
replace it in a copy of the APK, and sign that modified APK. This is optional developer tooling, not a player step.
