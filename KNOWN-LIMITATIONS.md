# Known limitations

This is an early release. The game has been tested through the first Downtown quests, but not much beyond arrival in
**Hollywood**, so later areas and quests may contain significant issues.

- Some animations are not yet faithful to the original game.
- Enemy AI and physics need further tuning.
- The user experience needs further improvements.
- The Nosferatu clan is not yet feature complete.
- Masquerade violations and Humanity loss currently occur only through dialogue
  checks; their other gameplay triggers are not implemented yet.

PC VR in 0.1.3:

- Character parallax is not ready: leave it Off. DLSS Ray Reconstruction works but costs too much frame time in VR for
  90 fps; use NRD. See the [recommended settings](INSTALL-WINDOWS.md#recommended-settings).
- Only NVIDIA RTX GPUs have been tested.
- The setup and the Companion are not signed yet, so Windows SmartScreen warns about them.
- Converting the RTX Remaster materials needs about 40 GB free while it runs.

Open issues carried from 0.1.2:

- Some weapon holds still need work (the female baton, torch and tire iron, the Chang blade's
  thumb, several pistol, SMG and shotgun two-hand holds, the frag grenade). The upper arm can sit
  in the armpit, a cupping arm can bend oddly, and a long gun in two hands can creep slowly.
- A fast two-hand swing with the fire axe can outrun the second hand.
- Weapon scopes and throwing grenades by hand are not done yet.
- Saves can't be deleted in the headset yet; delete them on the PC.
- Sounds, hints and scripted moves at a trigger's edge may repeat.
- Models with no face rig, such as Mike, Carl and Al, don't move their mouths.
- Only ball joints are simulated; props on other joint types stay still.
- In the parking garage, gunmen upstairs may stay idle while you fight their mates. A frenzy
  cannot yet end in feeding. Some scripted explosions deal no damage.
- Rare crashes have been reported in Downtown's hub and skyline maps.

Expect weekly releases. **Bug reports are crucial to development:** please use
the in-game reporting tool and describe what happened, where, and how to reproduce
it. Keep backups of your saves while testing.

Only the separately supplied, tested Unofficial Patch snapshot is the initial mod
pack target. Upstream patch versions newer than the
pack are not automatically compatible.
