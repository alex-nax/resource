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

[Installation instructions](instructions.md) - [Companion app](COMPANION.md) - [Controls](CONTROLS.md) -
[Known limitations](KNOWN-LIMITATIONS.md) - [Release notes](RELEASE-NOTES.md)

## Downloads

[Download the Vulkan APK and Unofficial Patch pack](https://github.com/alex-nax/resource/releases/latest).
Releases include SHA256 checksums and dependency source and license materials.
The APK filename follows `vtmb-re_source-MAJOR-MINOR-PATCH.apk`; the current
release is `vtmb-re_source-0-1-2.apk` (SemVer `0.1.2`). On Windows, the
[Companion app](COMPANION.md) installs and updates the game and the pack for you.
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

To play on a newer Unofficial Patch, make its pack from your own download with the
Companion: [Upgrading to Unofficial Patch 12.0](UPGRADE-UP12.md), with your saves.

## Credits

The **Unofficial Patch is authored by Werner Spahl (Wesp5)** with its credited
contributors. ReSource supplies the engine and packaging, not authorship of the
patch. [Wesp5's patch page](https://www.moddb.com/mods/vtmb-unofficial-patch).
The pack preserves his original readme and contributor acknowledgments.

Bloodlines is owned by its respective rights holders. This is an unofficial fan
project, not an official Troika, Activision or World of Darkness product.
See [third-party notices](THIRD-PARTY-NOTICES.md) and [licenses](licenses/README.md).

See the [changelog](CHANGELOG.md). Upgrading from 0.1.1 needs the new APK, installed as an
update without uninstalling, and the new Unofficial Patch pack.
