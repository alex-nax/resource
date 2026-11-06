# Release notes

## 0.1.2

Weapon grips on every weapon, enemies that run the original game's own AI rules, saves
kept in `/sdcard/vtmb/saves`, a new Unofficial Patch pack with Basic and Plus, and a
Windows [Companion app](COMPANION.md) that sets everything up. See the
[changelog](CHANGELOG.md) for the full list and the known issues.

**Upgrading from 0.1.1 needs the new APK and the new pack.** Install the APK as an
update; **do not uninstall 0.1.1 first**, because that deletes its private saves. Launch
it once with file access so your saves are copied to `/sdcard/vtmb/saves`, then copy the
new pack's `vtmb` contents into `/sdcard/vtmb`. The game asks for the new pack until it
is installed. The Companion does all of this with **Set up everything left**. Follow the
[installation instructions](instructions.md).

The Unofficial Patch is by **Werner Spahl (Wesp5)** and contributors. You need a legal
Steam or GOG copy of Bloodlines (2004).

## 0.1.1 hotfix

Fixes the Gimble intercom control lock, adds an optional first-person hair setting,
and includes the New Game fix in the updated Unofficial Patch pack. OpenAL is
now dynamically linked. See the [changelog](CHANGELOG.md) for details.

If you already installed the 0.1.0 pack and New Game fix, **install only the new
APK** over the existing app. Fresh installs need the APK and updated pack.
Follow the [installation instructions](instructions.md); retain your saves and
settings by keeping the existing app installed.

## Initial Quest Vulkan release

VtMB VR [re:Source] runs on Quest with your legally obtained Steam or GOG copy of
Vampire: The Masquerade - Bloodlines (2004). Install the APK, launch it to enable
file access and create `/sdcard/vtmb`, then copy the game and patch using SideQuest.
See [installation instructions](instructions.md).

The Unofficial Patch pack is by **Werner Spahl (Wesp5)** and contributors. It
includes ready-to-use compiled scripts; no compilation is needed on your computer.
Character shadows default to On, and live mirror reflections default to Off.
Both settings remain selectable; existing saved preferences are preserved.

Testing has not extended much beyond arrival in **Downtown**. Some animations
are not yet faithful; enemy AI, physics and UX need further work. Nosferatu is
not yet feature complete. Masquerade violations and Humanity loss currently
occur only through dialogue checks. See [known limitations](KNOWN-LIMITATIONS.md).

Expect weekly releases. **Bug reports are crucial to development.** Please use
the in-game report tool and include the location and steps to reproduce the issue.
Keep backups of your saves. Artifact checksums accompany each release.
