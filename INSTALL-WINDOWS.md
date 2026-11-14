# PC VR on Windows

VtMB VR [re:Source] 0.1.3 runs **Vampire: The Masquerade - Bloodlines (2004)** in VR on a Windows PC, with your
headset connected through Virtual Desktop, Quest Link / Air Link or SteamVR. It plays the original game's maps,
characters, dialogue and quests from your own copy, with the Unofficial Patch by Werner Spahl (Wesp5), and optional
graphics packs that add PBR materials, new lighting and ray-traced effects.

**You need a legal copy of Bloodlines from [Steam](https://store.steampowered.com/app/2600/) or
[GOG](https://www.gog.com/en/game/vampire_the_masquerade_bloodlines).** Nothing of the original game is included.
Bloodlines 2 is a different game and cannot supply these files.

## What you need

- Windows 10 or 11, 64-bit.
- A PC VR headset and an active **OpenXR runtime**: Virtual Desktop, Quest Link / Air Link, or SteamVR. Tested with a
  Quest 3 over Virtual Desktop.
- A Vulkan GPU. DLSS and the ray-traced effects are developed and tested on NVIDIA RTX (the numbers below are from an
  RTX 4070 Ti SUPER); the ray-traced rows need a GPU with Vulkan ray queries, and other GPUs are untested.
- Disk space, on the drive you install to:

| What | Download | On disk |
| --- | --- | --- |
| The game and the Companion | 82 MB | 0.3 GB |
| Your game files, copied | - | 2.8 GB |
| Unofficial Patch 11.5 (required) | 722 MB | 1.3 GB |
| PBR materials (generated) | 3.9 GB | 3.9 GB, about 12 GB free while it installs |
| RTX Remaster materials | 9.2 GB, from the mod's own page | 6 GB, about 40 GB free while it converts |
| MasterPBR lighting | 617 MB | 3.1 GB |
| MasterPBR ray-tracing add-on | 354 MB | under 1 GB |

The graphics packs are optional. The game is complete with only the Unofficial Patch.

## Install

1. **Download** `vtmb-vr-0.1.3-setup.exe` from the [release page](https://github.com/alex-nax/resource/releases/latest).
   To check it, run `Get-FileHash vtmb-vr-0.1.3-setup.exe` in PowerShell and compare the result with the release's
   `SHA256SUMS`.
2. **Run it.** The setup is not signed yet, so Windows SmartScreen may warn about an unknown publisher: choose
   **More info**, then **Run anyway**.
3. **Pick a folder.** The default, `%LOCALAPPDATA%\Programs\VtMB VR re-Source`, needs no administrator rights. Choose
   a drive with room for the packs you want. The setup refuses a folder that needs administrator rights (such as
   `Program Files`), because the game and the Companion write beside themselves, and a folder that already holds other
   files, because uninstalling removes the whole install folder.
4. When the setup finishes, the **Companion** opens on its **PCVR** tab. It shows "Checking this PC..." for a moment,
   then a numbered list. Do the steps in order; each one says what it found and what is left, shows its progress in
   percent while it works, and keeps any error on the step with a **Retry** button.

### The Companion's steps

1. **Install:** where the game is. Nothing to do.
2. **Game files:** press **Copy game files**. The Companion finds your Steam or GOG copy by itself. If it does not, or
   you want another copy, use **Browse...** to pick the folder that holds the game's `Vampire` folder, then
   **Use this folder**. Your own copy is only read, never changed. A stopped copy goes on where it stopped.
3. **Unofficial Patch:** press **Download and install Unofficial Patch 11.5**. It is our prepared pack of Wesp5's
   patch, the same one the Quest uses, so saves move between the two.
4. **Graphics packs (optional):**
   - **Install all for this PC** queues every pack your GPU can use; they download and install one at a time. You can
     also queue them one by one with **Install**.
   - **RTX Remaster materials** are made from the Bloodlines RTX Remaster mod, which we do not host. Press **Get the
     archive from the mod's page**, download `VTMB_RTX_Alpha_0_0_2.1.zip` (9.2 GB) there, then pick it with
     **Browse...** and press **Convert and install** (about 10 minutes on a fast PC). Convert waits until the PBR
     materials pack is installed, because it builds on it. The archive is checked against its file list first; a
     download that is missing files is refused with what is missing.
   - **MasterPBR** needs both material packs. Queue it whenever you like: it downloads first and installs when they
     are in. Its **ray-tracing add-on** needs MasterPBR and a GPU with ray queries.
5. **Saves (optional):** with your Quest connected over USB (see the **Setup** tab), **Import saves from Quest** brings
   your 0.1.x Quest saves to the PC, and **Send saves to Quest** takes them back. Nothing is overwritten: a different
   save with the same name gets a new slot.

Then put on the headset with your VR runtime running (Virtual Desktop, Link or SteamVR) and press **Play**. The game
starts in VR. If nothing happens, open the `logs` folder in the install folder: "no active OpenXR runtime" means the
headset was not connected or no OpenXR runtime is set as active.

### Turn the packs on in the game

Installed packs are off until you turn them on: in the game's main menu open **Mods** and switch on the packs you
installed. They apply when you close the Mods screen. Packs share your saves with the unmodded game, so you can switch them off
again at any time.

## Recommended settings

In the game, open **Options > Display**. Most of these need the graphics packs and a ray-tracing GPU; a row your PC or
your packs cannot use is greyed with the reason. "Applies when you close Options" means just that.

**Virtual Desktop (Quest 3):** in its Streaming tab set the frame rate to **90 fps**, turn **Synchronous Spacewarp
off**, and choose the **VR Graphics Quality** whose resolution is close to the headset panel (about 2064 x 2208 per eye
on a Quest 3). Higher tiers cost far more GPU time than they add in sharpness here.

**Sharpness**

| Setting | Recommended | Notes |
| --- | --- | --- |
| Upscaler | DLSS on NVIDIA RTX | FSR or XeSS on other GPUs |
| Upscale quality | DLAA on a fast GPU, otherwise Quality | DLAA renders at full size and is the sharpest |
| Ray tracing detail | Balanced | Full traces at full size: sharper, several ms slower |
| DLSS version | Automatic | DLSS 3 is faster and softer if you need frames |

**Lighting**

| Setting | Recommended | Notes |
| --- | --- | --- |
| Shadows | Ray-traced, otherwise Character | |
| Shadow quality | Medium | |
| Reflections | Ray-traced | Off saves the most time if you need frames |
| Lighting mode | Ray-traced | Lightmaps on GPUs without ray queries |
| Lighting quality | Low | Medium and High cost a lot more in VR for a small difference |
| Denoiser | **NRD** | See below |
| Live mirror reflections | **Off** | See below |
| Water caustics | On | |
| Baked lighting detail | On, with MasterPBR | |
| Local ambient | On | |

**Materials**

| Setting | Recommended | Notes |
| --- | --- | --- |
| PBR materials | On, with the packs | |
| Parallax | Off for 90 fps, On if you have headroom | |
| Character parallax | **Off** | See below |
| Bump-mapped world | Off | |

These hold 90 fps on an RTX 4070 Ti SUPER with a Quest 3 over Virtual Desktop.

### Leave these off

- **Character parallax: leave Off.** The characters' materials are not ready for it yet, and faces and clothing can
  look wrong with it on.
- **Denoiser: DLSS Ray Reconstruction: leave on NRD.** Ray Reconstruction looks cleaner, but in VR it costs about 9 ms
  more a frame at Quality and about 20 ms at DLAA (both eyes), which halves the frame rate.
- **Live mirror reflections: leave Off.** Rendering the mirror live costs a lot of frame time. Mirrors keep their
  reflections with it off.

## Updating and uninstalling

The Companion offers its own updates on the **Setup** tab (**Versions**). For a new game version, run the new setup
over the existing install; your game files, packs and saves stay.

Uninstall with **Uninstall VtMB VR re-Source** in the Start menu, or from Windows Settings > Apps. It removes the game, the Companion, the copied game files
and the installed packs, and asks whether to delete your saves and settings too; the default keeps them. Saves and
settings live in `%APPDATA%\vtmb-vr`.

## Licenses

See `LICENSE`, `THIRD-PARTY-NOTICES.md` and the `licenses` folder in the install folder.

## Reporting bugs

**Bug reports are crucial to development.** Use the in-game reporting tool (it attaches a save of the moment) and say
what happened, where, and how to reproduce it. See the [known limitations](KNOWN-LIMITATIONS.md) first.
