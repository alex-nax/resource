# Install VtMB VR [re:Source] on Quest

**Obtain a legal copy of Vampire: The Masquerade - Bloodlines (2004) from
[Steam](https://store.steampowered.com/app/2600/) or
[GOG](https://www.gog.com/en/game/vampire_the_masquerade_bloodlines), and install it
on your computer.** Bloodlines 2 is a different game.

**The easy way on Windows:** the [Companion app](COMPANION.md) does every step below over a USB cable,
and updates the game later. The steps below do the same by hand with SideQuest.

You need [SideQuest for your computer](https://sidequestvr.com/setup-howto),
a USB cable, and developer mode enabled on your Quest. Use SideQuest's desktop
installer with APK installation and headset file management.

1. **Download** the Vulkan APK and Unofficial Patch ZIP from
   [ReSource Releases](https://github.com/alex-nax/resource/releases).
2. **Install the APK** using SideQuest's APK installation button.
3. **Launch VtMB VR [re:Source] first** from the Quest's Unknown Sources apps.
   On the setup screen, choose **Allow game file access** and enable access in
   the system screen. Return to the app (or close and reopen it) so it creates
   `/sdcard/vtmb`. Then close the app before copying files.
4. **Extract the patch ZIP** on your computer. It contains a folder named `vtmb`.
   The patch is by **Werner Spahl (Wesp5)** and already includes all compiled scripts, ready to use.
   It holds both Basic and Plus; choose one in the game's Mods menu.
5. **Copy your game's entire `Vampire` folder** into that extracted `vtmb` folder,
   alongside `Unofficial_Patch`. Copy it; keep your original installation intact.
6. **Copy the contents of `vtmb` to the headset** with SideQuest's file manager.
   Open the existing `/sdcard/vtmb` folder and copy `Vampire`, `Unofficial_Patch`,
   `credits`, and `pack.json` into it. Wait for the transfer to finish.
7. **Reopen VtMB VR [re:Source]** to play.

Your headset should contain:

```text
/sdcard/vtmb/
  Vampire/                    <- your legal game's complete Vampire folder
  Unofficial_Patch/            <- the supplied Wesp5 patch
    python/                   <- compiled .pyc files already included
  credits/
  pack.json
```

If the setup screen remains, check that `Vampire/pack000.vpk` is directly inside
`/sdcard/vtmb/Vampire`, that file access is allowed, and that the copy completed.
If it says **File access required**, the game cannot write saves to
`/sdcard/vtmb/saves`: allow file access, or free up headset space, then restart the app.
Avoid an extra nested `vtmb/vtmb` folder. Restart after copying files.

## Updating from 0.1.1 to 0.1.2

0.1.2 needs **both** the new APK and the new Unofficial Patch pack.

1. **Install `vtmb-re_source-0-1-2.apk` as an update** over the existing app. **Do not
   uninstall 0.1.1 first:** uninstalling deletes its private saves.
2. **Launch it once** and allow file access if asked. Your saves are copied from the app's
   private storage to `/sdcard/vtmb/saves`. Then close the app.
3. **Install the new pack:** extract the new patch ZIP on your computer and copy the contents
   of its `vtmb` folder into `/sdcard/vtmb`, replacing when asked. Nothing needs deleting, and
   you do not need to copy `Vampire` again. Until the new pack is in place, the game asks for it.

The Companion does all three steps with **Set up everything left**.

See the [changelog](CHANGELOG.md) for what changed.

For updates, install the new APK over the existing app with SideQuest. Do not
uninstall the app or clear its storage: that removes its settings and the private
copy of older saves. Saves live in `/sdcard/vtmb/saves`, and a PC can copy them.
Keep a backup before changing patch versions. Use one supplied mod pack at a time.

Read the [known limitations](KNOWN-LIMITATIONS.md) before playing. Bug reports
through the in-game tool help guide the planned weekly releases.
