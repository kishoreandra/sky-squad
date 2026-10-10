# Sky Squad
An Android / iOS game inspired by Mini Militia, from the Sky Squad team at Arc Light Studio.

2D jetpack shooter made with Godot 4.3: bots, hotspot (LAN) play, online rooms with room codes, avatars in the Locker.

## Folders
- `main.gd`, `main.tscn`, `project.godot` – the game
- `art/`, `sfx/`, `fonts/` – pictures, sounds, fonts
- `server/` – the online room server (`roomd.py`, `setup.sh`)
- `scripts/` – tools that made the art and sounds
- `.github/workflows/ios.yml` – builds the iPhone app on GitHub's free Mac (Actions tab > iPhone build > Run workflow)

Never commit the Android signing key (`keys/`).
