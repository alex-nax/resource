# Unofficial Patch pack

**Author: Werner Spahl (Wesp5)**, with the contributors listed in the original
`VTMBup-readme.txt`. [Official patch page](https://www.moddb.com/mods/vtmb-unofficial-patch).
ReSource supplies the packaging and Python bytecode conversion.

This pack is built from the currently tested 11.5-generation local installation,
identified as `11.5-resource.20261106c-sidequest`. This label identifies our tested snapshot,
not a claim that it is Wesp5's latest upstream release.

The ZIP contains the patch data under `vtmb/Unofficial_Patch`, all **35** matching
compiled Python 2.1 modules alongside their sources under `vtmb/Unofficial_Patch/python`, the unchanged original
readme under `vtmb/credits`, and a file-by-file SHA256 manifest. It contains no original
`Vampire` directory, native game executables, saves or personal settings.

It holds both variants of the patch: the Basic files under `vtmb/Unofficial_Patch`, and what Plus changes or adds under
`vtmb/Unofficial_Patch/variants/plus`. Choose in the game's Mods menu; changing it needs a restart and a new campaign.
The Plus files come from Wesp5's own 11.5 installer, a later build of 11.5 than the Basic files, and include Plus's
own vehicle models (the LightningBird, Chevy Malibu, cargo truck, cop car and VW bus).

This pack is required from game version 0.1.2. `vtmb/Unofficial_Patch/derived` also holds two small data files extracted from the patch's
`vampire.dll` and `client.dll`: the NPC schedule tables and the terminal font. The DLLs themselves are not included,
and `pack.json` records the hash of each file the data came from.

The pack includes the startup configuration at `Unofficial_Patch/scripts/liblist.gam`,
which fixes New Game on clean installations; no separate fix ZIP is needed. Players
coming from 0.1.1 install this pack over the old one: game 0.1.2 needs it.

Obtain a **legal Steam/GOG copy of Bloodlines** separately, then follow
[the installation instructions](../../instructions.md). Keep Basic/Plus selection
within the modes supported by the in-game menu for this pack. Do not combine these
scripts with another patch generation or a different game-layer mod.
