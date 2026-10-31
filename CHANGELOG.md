# Changelog

## 0.1.1 - 2026-10-31

- Fixed controls remaining locked after Gimble's Prosthetics intercom dialogue.
  Shared dialogue cleanup also covers similar cinematic conversations while
  allowing an authored follow-up camera shot to continue.
- Added **First-person hair** under **Options > VR**, Off by default. Toggle the
  hair visible in your own view, including Gangrel and female Tremere. Mirrors
  and shadows keep the character's hair.
- Updated the Unofficial Patch pack to include the startup configuration that
  fixes New Game on clean installations. No separate New Game fix ZIP is needed.
- OpenAL is now a separate shared library. Developer downloads contain its source
  and build recipe, without an application relink archive.

**Upgrade:** if your 0.1.0 pack already has the New Game fix, install only the new
APK over the existing app. Keep your game files, saves and settings. Fresh installs
need the new APK and updated pack. See [installation instructions](instructions.md).

The Unofficial Patch is by **Werner Spahl (Wesp5)** and contributors.
[Known limitations](KNOWN-LIMITATIONS.md) still apply. In-game bug reports are
crucial to development; weekly releases are planned.

## 0.1.0 - 2026-10-30

Initial public Vulkan release for Quest 3, with a ready-to-use Unofficial Patch
pack and SideQuest installation. A small startup fix was added for New Game;
that fix is included in the 0.1.1 pack.
