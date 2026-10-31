# License materials

[The project MIT license](../LICENSE) covers original ReSource tools/code.
The Unofficial Patch archive carries its original readme and credits.

The dependency license texts in this directory were copied from the actual
Vulkan build inputs. [manifest.json](manifest.json) records their source revisions
and SHA256 values. These include OpenAL Soft, OpenXR, Jolt, GLM, mimalloc, miniz,
stb, dr_libs and microui.

The APK also contains these notices under `assets/third-party/`.
OpenAL Soft is dynamically linked as `libopenal.so` in 0.1.1 and later.
The matching `vtmb-re_source-0-1-1-openal-source.zip` contains its exact source,
local compatibility change and build recipe. This optional developer material
is not needed to install or play. Application object/relink archives are not
part of this release. Historical 0.1.0 relink materials remain with that release.
See [release assets](https://github.com/alex-nax/resource/releases/tag/v0.1.1).
