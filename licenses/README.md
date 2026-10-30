# License materials

[The project MIT license](../LICENSE) covers original ReSource tools/code.
The Unofficial Patch archive carries its original readme and credits.

The dependency license texts in this directory were copied from the actual
Vulkan build inputs. [manifest.json](manifest.json) records their source revisions
and SHA256 values. These include OpenAL Soft, OpenXR, Jolt, GLM, mimalloc, miniz,
stb, dr_libs and microui.

The APK also contains these notices under `assets/third-party/`.
OpenAL Soft is statically linked. The matching
`vtmb-re_source-0-1-0-openal-relink.zip` release asset contains its source, local
compatibility patch, application object files, other required static libraries,
and a portable relink recipe. This optional developer kit is not needed to play.
See [release assets](https://github.com/alex-nax/resource/releases/tag/v0.1.0).
