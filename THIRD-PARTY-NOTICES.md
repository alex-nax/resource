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

The Windows companion app also ships Microsoft's **texconv** from DirectXTex 2026.5.8.1 (MIT), unchanged and
Microsoft-signed (`texconv.exe`, SHA-256 `dcfdec10244e02cf5037fba089c55fb7e1326b1c8181742d77d15fa5cb5eef06`). It is
a separate program the app runs to compress the maps of the RTX Remaster import. Source:
<https://github.com/microsoft/DirectXTex>. The import's texture hash is xxHash (BSD 2-Clause) by Yann Collet.

The companion app is built with SDL3 (zlib), microui and miniz (MIT), stb (MIT or public domain) and the Vulkan
headers (Apache 2.0), and embeds the Inter font (SIL OFL 1.1). The Windows zip carries Microsoft's C++ runtime DLLs,
redistributed under the Visual Studio terms. The Mac zip carries MoltenVK (Apache 2.0). Their texts are in its
`licenses` folder.

Dependency notices are included in the APK and in [licenses/](licenses/README.md).
OpenAL Soft is dynamically linked. Its matching source, local changes and build
recipe accompany the release assets; no application relink archive is needed.

PC builds with ray tracing (desktop Vulkan, built with `VTMB_NRD`) include **NVIDIA Real-Time Denoisers (NRD)
v4.18.0** (<https://github.com/NVIDIA-RTX/NRD>, commit `8f12a22fc90e6a3c7f5da4c9c3103633c842963a`) in object code
inside the application. NRD is under the **NVIDIA RTX SDKs License**, not the MIT license; those portions keep
NVIDIA's terms, and the project's MIT license does not relicense them. NRD's source is fetched at build time and is
not part of our repository or releases. NRD builds with NVIDIA's MathLib v11 and ShaderMake (`3f01623a`), both MIT.
The three texts are in [licenses/nrd/](licenses/nrd/LICENSE.txt). The Quest APK does not include NRD.

The Windows PC setup carries, beside the game, OpenAL Soft as `OpenAL32.dll` (LGPL 2.1, dynamically linked; you may
replace it), Microsoft's C++ runtime DLLs (redistributed under the Visual Studio terms), and three upscalers, each
unmodified and under its own terms: AMD FidelityFX FSR 3.1 (MIT, compiled into the game), NVIDIA DLSS
(`nvngx_dlss.dll`, `nvngx_dlssd.dll`; NVIDIA RTX SDKs License) and Intel XeSS (`libxess.dll`; Intel Simplified
Software License). Their texts, and NRD's with the note of our one change to it, are in the `licenses` folder of the
install.
