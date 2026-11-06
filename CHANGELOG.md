# Changelog

## 0.1.2 - 2026-11-06

**Upgrading from 0.1.1:** install the new APK as an update, without uninstalling, and install the new
Unofficial Patch pack: 0.1.2 needs it. Your saves are copied to `/sdcard/vtmb/saves` on the first launch with
file access. See the [installation instructions](instructions.md), or let the [Companion](COMPANION.md) do it.

#### VR weapons

- **Grips on every weapon, for both bodies:** each weapon sits in the hand the way the original's characters hold it,
  with the fingers closed on the handle and the elbow bending naturally.
- **Two-hand holds:** long melee weapons and long guns take the two-hand stance the original's characters use. Pistols
  and short SMGs are cupped by the other hand.
- **Blades in the left hand:** the knife's and katana's edge faces the target, not you.
- **Gun aim:** the second hand no longer pulls the hand that holds the gun, and the crosshair is drawn along the
  barrel, where the shot goes.
- **Steadier guns:** a held gun no longer shakes in the hand.

#### Enemies and characters

Characters now run the original game's own AI rules, read from its code, instead of approximations.

- **Schedules and tasks:** NPCs follow the original game's schedule and task lists, so they patrol, investigate, hunt, take cover, flee and cower as in the original.
- **One navigator for all movement:** characters plan routes on the map's own node graph, open doors on the way, step up and down ledges, cross narrow gaps, jump where the map allows it and stop at edges they can't cross.
- **Senses:** the original sight cone (157 degrees), the original light-based stealth, and hearing. Gunshots and fights are heard and investigated.
- **Gunshots are followed up:** enemies who hear your shot run to where it came from.
- **Memory and the hunt:** an enemy who loses sight of you searches where he last saw you, looks around, and gives up after the original's delays.
- **Melee groups:** enemies take turns to attack. When three or more fight you, the ones waiting take over after a
  combo instead of standing and watching; while they wait they circle and hold their weapons ready. Step-backs and retreats stop at furniture.
- **Gunmen:** they use cover, step back to shoot, and fire SMG bursts like the original (MAC-10, Uzi, Steyr). NPC bullets deal the original's damage.
- **Reactions:** enemies respond to being hit with the original's rules. NPCs fight each other according to their factions. Civilians flee crimes and Nosferatu, and witnesses send the street cops to the place of the crime.
- **Frenzy:** you can frenzy from hunger, with a red pulse and loss of control. A new game clears frenzy.
- **Life on the streets:** pedestrians walk their paths and wait at crosswalks. Hub characters vary their idles and turn in place properly. Heads look at what they talk to and what catches their eye. Mouths move for voices played by the map, using the Unofficial Patch's lipsync files.
- **Specific characters:** dogs chase and bite. Ghouls fight with claws. Grout's crouchers stand and idle on the floor. The warehouse wolf crosses the fence. Rats keep to their usual movement when they hear a gunshot.
- **Performance:** distant NPCs think less often, as in the original, so big hubs stay smooth.

#### World and physics

- **Explosions:** gas cans and other props the game marks as explosive blow up when broken, and the blast damages
  what is around them.
- **The warehouse crane** carries its hook and container, and drops the container when it stops. Props held by
  ball joints, such as the crane's hook, are simulated.
- **Triggers** fire on every touch, as in the original, so rain on the pier stays on.

#### Saves

- **Saves you can see and keep:** saves live in `/sdcard/vtmb/saves`, outside the app, so they survive reinstalls and can be backed up. Existing saves are copied there by themselves.
- **One folder per patch:** each patch and variant has its own readable save folder, such as `unofficial_patch-plus-11.5`.
- **0.1.1 saves on Plus:** saves from 0.1.1 load with the new pack's Plus files. Where Plus's smaller magazine can't
  hold a saved gun's rounds, the extra rounds go to your reserve. A save whose magazine is over by more than a whole
  magazine is refused as damaged, with a message.
- **Save conversion:** the Companion's command-line tool converts saves between the original game and this port, in both directions.
- **Outfit changes after loading:** a scripted outfit change, such as Heather's, takes effect after you load a save.
- **Unreadable saves are shown:** a save the game can't read is shown in Load Game as a greyed-out row saying why
  ("Can't be read by this build" or "Made by a newer build", with its date), instead of disappearing.

#### The Unofficial Patch pack

- **Required from 0.1.2:** the game asks for the new pack until it is installed.
- **Basic and Plus:** both variants are in the pack, and the Mods menu chooses which files load, not only which scripts run.
- **No DLLs:** the pack carries no DLLs. The data the game needs from them is extracted into the pack.
- **Plus's own vehicles:** the LightningBird, Chevy Malibu, cargo truck, cop car and VW bus use Plus's own models.

#### Graphics

- **Reflections and decals:** world reflections (`$envmap`) and map decals are drawn, and bump mapping is an option, off by default.
- **Fixed rendering bugs:**
  - blood no longer leaves a black square on walls
  - see-through surfaces draw in the right order
  - water moves smoothly
- **Sky and effects:**
  - the 3D sky no longer clips as you turn your head
  - sky particles and the plane's lights fly smoothly
  - the Tremere window glows
  - the lever room's lightning draws
- **HUD:** indicators stay level when you tilt your head.
- **Models:** models the map marks as hidden stay hidden.

#### Gameplay and interface

- **Character sheet:** shows carried artifacts and five dots with bonus art. Masquerade shows crossed-out masks.
- **Elysium:** no holstered weapons are shown.
- **Armor:** it is equipped and protects as authored.
- **Vendors:** stock follows the original's rules.
- **Quests and scripts:** scripted sequences, Knox's hand-in, moving platforms, hidden brushes and visibility inputs work as authored.
- **MSAA option:** turning MSAA off in Options no longer hides the option, so it can be turned back on.

#### Companion app (new, Windows)

- **Setup:** one place to install everything over USB. It finds your legal copy (Steam, GOG, or GOG's offline
  installer), installs or updates the game, copies the game files and installs the patch pack. It shows only the
  current step, with a progress bar.
- **Changelog:** a button shows every release's notes.
- **Updates:** the Companion offers new game releases and updates itself.
- Windows x64 only for now; there is no Mac package.

#### Known issues

- **Weapon grips:** some holds still need work: the female baton, torch and tire iron grips, the Chang blade's
  thumb, the Anaconda, Desert Eagle, Glock, MAC-10, Uzi and flamethrower holds, the .38's left hand, the super
  shotgun, the M37 and the frag grenade. The upper arm can sit in the armpit. The cupping arm can bend oddly, and a
  long gun held in two hands can creep slowly while you stand still.
- **Fire axe:** a fast two-hand swing can outrun the second hand.
- **Not done yet:** weapon scopes, and throwing grenades by hand.
- **Deleting saves:** saves can't be deleted in the headset yet; delete them on the PC.
- **Triggers:** because triggers now fire on every touch, sounds, hints and scripted moves at a trigger's edge may repeat.
- **Lipsync:** models with no face rig, such as Mike, Carl and Al, don't move their mouths.
- **Physics:** only ball joints are simulated, so props held by other joint types stay still. Some scripted
  explosions deal no damage.
- **Enemies:** in the parking garage, gunmen upstairs may stay idle while you fight their mates. A frenzy cannot
  yet end in feeding.
- **Crashes:** rare crashes have been reported in Downtown's hub and skyline maps.
- **Testing:** the game has not been tested much beyond arrival in Downtown.

The Unofficial Patch is by **Werner Spahl (Wesp5)** and contributors. You need a legal copy of
Bloodlines (2004) from Steam or GOG. In-game bug reports are crucial to development.

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
