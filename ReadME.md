# Snakey Boi

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [How to Play](#how-to-play)
6. [Game Modes](#game-modes)
7. [Power-ups](#power-ups)
8. [Customization](#customization)
9. [High Scores](#high-scores)
10. [File Structure](#file-structure)
11. [Contributing](#contributing)
12. [License](#license)

## Introduction

Snakey Boi is a modern take on the classic Snake game, implemented in Python using the Pygame library. This version includes additional features such as power-ups, different game modes, and customizable settings to enhance the gaming experience.

## Features

- Classic Snake gameplay
- Multiple game modes (Classic and Time Attack)
- Power-ups with unique effects
- Customizable controls
- Adjustable difficulty levels
- Multiple color schemes
- High score tracking

## Requirements

- Python 3.7+
- Pygame 2.0+

## Installation

1. Clone the repository:

```git clone https://github.com/IAmJuniorB/snakey-boi.git```


2. Navigate to the project directory:

```cd snakey-boi```


3. Install the required dependencies:

```pip install -r requirements.txt```


4. Run the game:

```python main.py```


## How to Play

- Use the WASD keys to control the snake's direction:
- W: Up
- A: Left
- S: Down
- D: Right
- Eat the food to grow longer and increase your score
- Avoid colliding with the walls or the snake's own body
- Collect power-ups for temporary advantages
- - I would argue that one of the powerups is a disadvantage

## Game Modes

1. **Classic Mode**: Play indefinitely and try to achieve the highest score possible.
2. **Time Attack Mode**: Race against the clock to get the highest score within the time limit.

## Power-ups

- **Speed Boost (Triangle)**: Temporarily increases the snake's speed.
- **Score Multiplier (Square)**: Doubles the points earned for a short duration.
- **Invincibility (Circle)**: Makes the snake invulnerable to collisions for a brief period.

## Customization

- **Difficulty Levels**: Choose between Easy, Medium, and Hard difficulties. Starts you automatically in medium mode.
- **Color Schemes**: Select from Default, Monochrome, or Neon color schemes. (These could be better honestly)
- **Controls**: Customize the control keys in the options menu.

## High Scores

The game keeps track of the top 5 high scores. After each game, if your score qualifies, you'll be prompted to enter your name for the high score list.

(Currently having issues with this part)

## File Structure

- `main.py`: The main entry point of the game.
- `game.py`: Contains the core game logic and loop.
- `menu.py`: Handles the menu system and user interface.
- `settings.py`: Manages game settings and configurations.
- `high_scores.json`: Stores the high scores (created after the first high score is recorded).

## Contributing

Contributions to Snakey Boi are welcome! Please feel free to submit pull requests, create issues or spread the word.

## License

This project is licensed under the MIT License - see the [LICENSE](license.txt) file for details.

---

Enjoy playing Snakey Boi! If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository or email me at jbonfan@wgu.edu.

