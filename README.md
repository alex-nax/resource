# VtMB VR [re:Source]

ReSource is a replacement engine for **Vampire: The Masquerade - Bloodlines (2004)** that plays the original game in
virtual reality: **PC VR on Windows** and standalone on **Meta Quest**. It runs the original game's maps, characters,
dialogue and quests from your own copy, with melee and guns in your hands, world-space dialogue and menus, and
optional graphics packs with PBR materials, new lighting and ray-traced effects on PC.

This is an early release. Please read the [known limitations](KNOWN-LIMITATIONS.md) before playing.

**You must obtain a legal copy of the original game from
[Steam](https://store.steampowered.com/app/2600/) or
[GOG](https://www.gog.com/en/game/vampire_the_masquerade_bloodlines).**
The engine and mod packs do not include the original game and do not replace buying it.
Bloodlines 2 is a different game and cannot supply these files.

## Get started

- **PC VR (Windows): new in 0.1.3.** Download `vtmb-vr-0.1.3-setup.exe` from the
  [latest release](https://github.com/alex-nax/resource/releases/latest) and follow the
  [PC VR guide](INSTALL-WINDOWS.md): the setup installs the game and the Companion app, and the Companion copies your
  game files, installs the Unofficial Patch and the optional graphics packs, step by step. The guide also lists the
  recommended settings and the ones to leave off.
- **Quest:** the current Quest release is 0.1.2; Quest 0.1.3 follows shortly. Follow the
  [Quest installation instructions](instructions.md), or let the [Companion app](COMPANION.md) do it over USB.

[PC VR guide](INSTALL-WINDOWS.md) - [Quest instructions](instructions.md) - [Companion app](COMPANION.md) -
[Controls](CONTROLS.md) - [Known limitations](KNOWN-LIMITATIONS.md) - [Release notes](RELEASE-NOTES.md) -
[Changelog](CHANGELOG.md)

Saves move between the PC and the Quest: the Companion imports Quest saves to the PC and sends them back, without
overwriting any.

## Downloads

All downloads are on the [releases page](https://github.com/alex-nax/resource/releases). Releases include SHA256
checksums and dependency source and license materials. The Quest APK filename follows
`vtmb-re_source-MAJOR-MINOR-PATCH.apk`; the Windows setup is `vtmb-vr-MAJOR.MINOR.PATCH-setup.exe`. GitHub's automatic
source-code ZIP is documentation and tools, not an installed game.

Expect regular releases. **Bug reports are crucial to development.** Please use the in-game reporting tool and include
the location and steps to reproduce.

## Mod packs

| Pack | Author | Platforms | Status |
| --- | --- | --- | --- |
| [Unofficial Patch](packs/unofficial-patch/README.md) | Werner Spahl (**Wesp5**) and contributors | PC VR, Quest | Required; ready-to-use pack with compiled scripts |
| PBR materials (generated) | ReSource | PC VR | Optional; normal and specular maps generated from your own textures |
| RTX Remaster materials | The Bloodlines RTX Remaster mod's authors | PC VR | Optional; converted on your PC from the mod's own download, which we do not host |
| MasterPBR lighting and ray-tracing add-on | ReSource | PC VR | Optional; our baked lighting, applied to your own maps |

The Unofficial Patch pack contains its matching compiled Python scripts, credits and file checksums. Install one
supported game layer at a time; do not mix scripts from different mods or patch releases. See the
[pack catalog](packs/catalog.json). On PC, the Companion installs the packs, and you turn the graphics packs on in the
game's Mods menu; they share your saves with the unmodded game.

## Credits

The **Unofficial Patch is authored by Werner Spahl (Wesp5)** with its credited
contributors. ReSource supplies the engine and packaging, not authorship of the
patch. [Wesp5's patch page](https://www.moddb.com/mods/vtmb-unofficial-patch).
The pack preserves his original readme and contributor acknowledgments.

The RTX Remaster materials come from the
[Bloodlines RTX Remaster](https://www.moddb.com/mods/vampire-the-masquerade-bloodlines-rtx-remaster) mod by its
authors; you download it from its own page and the Companion converts it on your PC.

Bloodlines is owned by its respective rights holders. This is an unofficial fan
project, not an official Troika, Activision or World of Darkness product.
See [third-party notices](THIRD-PARTY-NOTICES.md) and [licenses](licenses/README.md).
