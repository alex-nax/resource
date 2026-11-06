# Third-party notices

ReSource's original code and tools are MIT licensed; see [LICENSE](LICENSE).
That license does not cover the original game or community mod content.

The Unofficial Patch is by **Werner Spahl (Wesp5)** and contributors. Its pack
includes the original `VTMBup-readme.txt` and acknowledgments unchanged. Patch
content remains under its authors' terms. Packaging and bytecode compilation do
not transfer authorship or make it MIT licensed.

Steam/GOG game files are supplied by each player and are not included in the pack.
The offline script compiler uses the player's own `vampire_python21.dll`; this DLL
and the original engine executables are not shipped with these tools.

The Windows companion app ships **innoextract 1.9** by Daniel Scharrer, unchanged, as
upstream's release build (`innoextract.exe`, SHA-256
`946bd06d8b3722a791fea4d84f496139eef6faef61640924cb72f5f1998a68e1`). It is a separate
program the app runs to unpack installers. It is under its own zlib-style license
and statically includes Boost (BSL 1.0), liblzma (public domain) and libstdc++ (GPL 3
with the GCC Runtime Library Exception). Those texts are in the `innoextract-licenses`
folder beside the app. Source: <https://constexpr.org/innoextract/>.

The companion app is built with SDL3 (zlib), microui and miniz (MIT), stb (MIT or public domain) and the Vulkan
headers (Apache 2.0), and embeds the Inter font (SIL OFL 1.1). The Windows zip carries Microsoft's C++ runtime DLLs,
redistributed under the Visual Studio terms. The Mac zip carries MoltenVK (Apache 2.0). Their texts are in its
`licenses` folder.

Dependency notices are included in the APK and in [licenses/](licenses/README.md).
OpenAL Soft is dynamically linked. Its matching source, local changes and build
recipe accompany the release assets; no application relink archive is needed.
