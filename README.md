# VtMB VR [re:Source]

An early Quest release. Please read the [known limitations](KNOWN-LIMITATIONS.md)
before playing. Testing has not extended much beyond arrival in Downtown.

ReSource is a replacement engine for **Vampire: The Masquerade - Bloodlines (2004)**,
with standalone VR on Meta Quest. The Quest distribution uses Vulkan.

**You must obtain a legal copy of the original game from
[Steam](https://store.steampowered.com/app/2600/) or
[GOG](https://www.gog.com/en/game/vampire_the_masquerade_bloodlines).**
The engine and mod packs do not include the original game and do not replace buying it.
Bloodlines 2 is a different game and cannot supply these files.

[Installation instructions](instructions.md) - [Controls](CONTROLS.md) -
[Known limitations](KNOWN-LIMITATIONS.md) - [Release notes](RELEASE-NOTES.md)

## Downloads

[Download the Vulkan APK and Unofficial Patch pack](https://github.com/alex-nax/resource/releases/latest).
Releases include SHA256 checksums and dependency source/relink materials.
The APK filename follows `vtmb-re_source-MAJOR-MINOR-PATCH.apk`; the initial
release is `vtmb-re_source-0-1-0.apk` (SemVer `0.1.0`).
GitHub's automatic source-code ZIP is documentation/tools, not an installed game.

Expect weekly releases. **Bug reports are crucial to development.** Please use
the in-game reporting tool and include the location and steps to reproduce.

## Mod packs

| Pack | Author | Status |
| --- | --- | --- |
| [Unofficial Patch](packs/unofficial-patch/README.md) | Werner Spahl (**Wesp5**) and contributors | Ready-to-use pack with compiled scripts |

The supplied pack contains its matching compiled Python scripts, credits
and file checksums. Install one supported game layer at a time; do not mix scripts
from different mods or patch releases. See the [pack catalog](packs/catalog.json).

## Credits

The **Unofficial Patch is authored by Werner Spahl (Wesp5)** with its credited
contributors. ReSource supplies the engine and packaging, not authorship of the
patch. [Wesp5's patch page](https://www.moddb.com/mods/vtmb-unofficial-patch).
The pack preserves his original readme and contributor acknowledgments.

Bloodlines is owned by its respective rights holders. This is an unofficial fan
project, not an official Troika, Activision or World of Darkness product.
See [third-party notices](THIRD-PARTY-NOTICES.md) and [licenses](licenses/README.md).
