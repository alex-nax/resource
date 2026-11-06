# VtMB VR [re:Source] Companion

The Companion is a small desktop app for Windows (x64). There is no Mac package yet. It sets the game up on your Quest over a USB cable: it installs the game, copies the game files from your own legal copy, and installs the Unofficial Patch pack. It never starts anything on the headset and never removes anything from it. Your saves stay where they are.

You need a legal copy of Bloodlines (2004) from Steam or GOG. The Companion never asks for your Steam password or a Steam Guard code.

## Get it

Download `vtmb-companion-0-2-0-windows-x64.zip` from the [releases page](https://github.com/alex-nax/resource/releases), and unpack it to a folder you can write to. Keep the files together.

Run `vtmb-companion.exe`. Windows may warn about an unknown publisher, because the app is not signed: choose **More info**, then **Run anyway**.

Check the download against the release's `SHA256SUMS` file if you want to be sure of it.

## Set up

1. Turn on developer mode on your Quest, connect the cable, and allow USB debugging in the headset.
2. Open the **Setup** tab. Each row says what it found and what is left.
3. Press **Set up everything left**. It tells you the sizes first, and stops if it needs you.
4. When it says **Ready**, start the game from the headset.

## Coming from 0.1.1

Version 0.1.2 of the game needs the new pack, and it will ask for a pack update until it has one. Open the Companion and press **Set up everything left**: it updates the game in place, then puts the new pack over the old one. Your saves, settings and game files stay.

Without the Companion: install the new APK with SideQuest, extract the new pack on your computer, and copy the contents of its `vtmb` folder into `/sdcard/vtmb`, replacing when asked.

Never uninstall the game to update it. Uninstalling erases its private saves.

## Updating the Companion

The **Versions** section of the Setup tab offers a newer Companion when there is one. Press **Update this app**. It checks the download's hash and replaces itself; if anything goes wrong, the version you have stays. Then close it and open it again.

## Saves between the original game and this port

The command-line tool beside the app converts saves in both directions. Run it from the Companion's folder.
`--out` names the new save file to write; use a new name, and keep your original save:

```
vtmb-companion-cli save-to-port <original .sav> --out <new .vtmbsave>
vtmb-companion-cli save-to-vanilla <port .vtmbsave> --template <an original .sav> --out <new .sav>
```

## Licenses

See `THIRD-PARTY-NOTICES.md` and the `licenses` folder beside the app.
