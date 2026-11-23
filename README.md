## Pacman_2024
Made during my first year in 2024


# Pac-Man Game

A Python Pac-Man-style game with a graphical launcher and three playable modes.

## Basic UI

When the game starts, the main menu appears with:

- **START GAME**: Opens the game mode selection screen
- **OPTIONS**: Opens the guide and high-score email options
- **EXIT GAME**: Opens the goodbye screen and closes the game
- **GO BACK**: Returns to the previous menu

The mode selection screen provides **CLASSIC**, **INTERMEDIATE**, and **SURVIVAL**.

## Game Modes

### Classic

The classic maze mode includes Pac-Man, four ghosts, dots, power pellets, lives, and score tracking.

- Move with `W`, `A`, `S`, `D` or the arrow keys
- Pause or resume with `P` or `Escape`
- Eat dots and power pellets
- Avoid ghosts unless a power pellet is active
- Clear the maze to complete the level

### Intermediate

The intermediate mode uses a larger tile-based maze and additional level mechanics.

- Move with `W`, `A`, `S`, `D` or the arrow keys
- Pause or resume with `P` or `Space`
- Quit with `Q` or `Escape`
- Collect dots and power pellets
- Avoid or attack ghosts
- Progress through levels and collect the highest possible score

### Survival

Survival mode is a separate Pygame Zero game with a timed maze challenge.

- Move with `W`, `A`, `S`, `D` or the arrow keys
- Pause or resume with `P`
- Restart with `R` while paused
- Quit with `Q` while paused
- Collect dots and avoid ghosts
- Lose lives through repeated ghost collisions

## Requirements

Install the required Python packages:

```powershell
py -m pip install -r requirements.txt
```

## Running the Game

From the project folder, run:

```powershell
py "Pacman Final (Main).py"
```

Classic and Intermediate can also be opened as standalone Pygame files:

```powershell
py Classic.py
py "Intermediate level.py"
```

Survival can be opened directly:

```powershell
py Survival.py
```

## Project Files

- `Pacman Final (Main).py`: Main launcher and integrated game modes
- `Classic.py`: Standalone classic mode
- `Intermediate level.py`: Standalone intermediate mode
- `Survival.py`: Standalone survival mode
- `boards.py`: Classic maze layout
- `map.py`: Survival maze movement and dot-map helpers
- `input.py`: Keyboard and joystick input helpers
- `assets/`, `gif/`, `images/`: Images, animations, sounds, boards, and game sprites
