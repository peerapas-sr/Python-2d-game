# 2D Shooting Game

A small top-down 2D arcade shooter made with Python and Pygame. The player explores a tiled map, shoots slime enemies, avoids collisions, and tries to survive as long as possible while increasing the score.

## Gameplay

- Move: W, A, S, D
- Shoot: Arrow keys
- Restart after losing: Enter
- Goal: defeat slimes by hitting them with bullets and avoid touching enemies

## Features

- Tile-based map and collision system
- Player movement and animation
- Enemy spawning and combat
- Score tracking and game-over restart flow
- Audio effects and background music
- Windows executable build included in the repository

## Project Structure

- `Code/Maingame.py` — main game loop and gameplay logic
- `Code/Player.py` — player character logic
- `Code/Spritesfile.py` — sprite and entity classes
- `Code/settings.py` — game settings and constants
- `Maps/` — Tiled map files and tilesets
- `sprites/` — characters, particles, and animation assets
- `audio/` — sound effects and music
- `GameLauncher.exe` — packaged Windows game build
- `Maingame.spec` — PyInstaller specification for building the app

## Requirements

- Python 3.10+
- `pygame`
- `pytmx`

Install dependencies:

```bash
pip install pygame pytmx
```

## Run the Game

From the repository root:

```bash
python Code/Maingame.py
```

You can also run the packaged Windows executable if available in the project root.

## Notes

This project was created as a simple game prototype and includes asset folders for the map, characters, and sound effects. The game is intended to be run locally on a desktop machine.
