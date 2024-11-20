"""
This module handles the configuration and initialization of the game screen and settings.
It imports necessary libraries and constants, and sets up the screen dimensions and other game settings.
"""
from typing import Dict, List, Tuple
import json
import os
import pygame

# Screen settings
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
FPS: int = 60

# Colors
BACKGROUND_COLOR: Tuple[int, int, int] = (0, 0, 100)  # Dark blue
WHITE: Tuple[int, int, int] = (255, 255, 255)
BLACK: Tuple[int, int, int] = (0, 0, 0)
RED: Tuple[int, int, int] = (255, 0, 0)
GREEN: Tuple[int, int, int] = (0, 255, 0)

# Game states
STATE_MENU: str = "menu"
STATE_GAME: str = "game"
STATE_HIGH_SCORES: str = "high_scores"
STATE_INSTRUCTIONS: str = "instructions"
STATE_OPTIONS: str = "options"

# Game settings
SNAKE_SIZE: int = 20
SNAKE_SPEED: int = 150  # Milliseconds between moves (lower is faster)

# Difficulty levels
DIFFICULTY_EASY: str = 'Easy'
DIFFICULTY_MEDIUM: str = 'Medium'
DIFFICULTY_HARD: str = 'Hard'

# Snake speeds for different difficulties. Try it on 1.
SNAKE_SPEED_EASY: int = 100
SNAKE_SPEED_MEDIUM: int = 50
SNAKE_SPEED_HARD: int = 25

# Color schemes
COLOR_SCHEMES: Dict[str, Dict[str, Tuple[int, int, int]]] = {
    'Default': {
        'background': (0, 0, 100),  # Dark blue
        'snake': (0, 255, 0),  # Green
        'food': (255, 0, 0),  # Red
    },
    'Monochrome': {
        'background': (0, 0, 0),  # Black
        'snake': (255, 255, 255),  # White
        'food': (128, 128, 128),  # Gray
    },
    'Neon': {
        'background': (0, 0, 0),  # Black
        'snake': (0, 255, 255),  # Cyan
        'food': (255, 0, 255),  # Magenta
    }
}

# Default controls
DEFAULT_CONTROLS: Dict[str, int] = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d
}

# Game modes
GAME_MODE_CLASSIC: str = "Classic"
GAME_MODE_TIME_ATTACK: str = "Time Attack"

# Power-up types
POWERUP_SPEED = "speed"
POWERUP_MULTIPLIER = "multiplier"
POWERUP_INVINCIBILITY = "invincibility"

# Power-up shapes
POWERUP_SHAPES = {
    POWERUP_SPEED: "triangle",
    POWERUP_MULTIPLIER: "square",
    POWERUP_INVINCIBILITY: "circle"
}

# Power-up durations (in seconds)
POWERUP_DURATION = {
    POWERUP_SPEED: 5,
    POWERUP_MULTIPLIER: 10,
    POWERUP_INVINCIBILITY: 7
}

# Power-up colors
POWERUP_COLORS = {
    POWERUP_SPEED: (255, 255, 0),  # Yellow
    POWERUP_MULTIPLIER: (255, 165, 0),  # Orange
    POWERUP_INVINCIBILITY: (138, 43, 226)  # Purple
}

# Power-up spawn interval (in seconds) I'll probably change this to random.randint
POWERUP_SPAWN_INTERVAL = 15

class GameSettings:
    """
    A class to manage game settings.
    """
    def __init__(self):
        """
        Initialize the GameSettings object with default values.
        """
        self.difficulty: str = DIFFICULTY_MEDIUM
        self.snake_speed: int = SNAKE_SPEED_MEDIUM
        self.color_scheme: str = 'Default'
        self.controls: Dict[str, int] = DEFAULT_CONTROLS.copy()
        self.game_mode: str = GAME_MODE_CLASSIC
        self.time_attack_duration: int = 60  # 60 seconds for Time Attack mode
        self.powerups_enabled: bool = True

    def set_difficulty(self, difficulty: str) -> None:
        """
        Set the game difficulty and adjust snake speed accordingly.
        Args:
            difficulty (str): The difficulty level to set.
        """
        self.difficulty = difficulty
        if difficulty == DIFFICULTY_EASY:
            self.snake_speed = SNAKE_SPEED_EASY
        elif difficulty == DIFFICULTY_MEDIUM:
            self.snake_speed = SNAKE_SPEED_MEDIUM
        else:
            self.snake_speed = SNAKE_SPEED_HARD

    def set_color_scheme(self, scheme: str) -> None:
        """
        Set the color scheme for the game.
        Args:
            scheme (str): The name of the color scheme to set.
        """
        if scheme in COLOR_SCHEMES:
            self.color_scheme = scheme

    def set_control(self, action: str, key: int) -> None:
        """
        Set a control key for a specific action.
        Args:
            action (str): The action to set the control for.
            key (int): The pygame key code to set for the action.
        """
        if action in self.controls:
            self.controls[action] = key

    def set_game_mode(self, mode: str) -> None:
        """
        Set the game mode.
        Args:
            mode (str): The game mode to set.
        """
        if mode in [GAME_MODE_CLASSIC, GAME_MODE_TIME_ATTACK]:
            self.game_mode = mode

    def toggle_powerups(self) -> None:
        """
        Toggle power-ups on or off.
        """
        self.powerups_enabled = not self.powerups_enabled

def load_high_scores():
    """
    Load the high scores from a JSON file.
    If the file doesn't exist, initialize an empty high scores list.

    Returns:
        List[Tuple[str, int]]: A list of tuples containing player names and scores.
    """
    global high_scores
    file_path = os.path.join(os.path.dirname(__file__), 'high_scores.json')
    try:
        with open(file_path, 'r') as f:
            high_scores = json.load(f)
        high_scores = [tuple(score) for score in high_scores]  # Convert lists to tuples...or try your best
        print(f"Loaded high scores: {high_scores}")
    except (FileNotFoundError, json.JSONDecodeError):
        high_scores = []
        print("No high scores file found or error decoding, starting with empty list")
    return high_scores

def save_high_scores():
    """
    Save the high scores to a JSON file.
    """
    global high_scores
    file_path = os.path.join(os.path.dirname(__file__), 'high_scores.json')
    with open(file_path, 'w') as f:
        json.dump(high_scores, f)
    print(f"Saved high scores: {high_scores}")

def reload_high_scores():
    """
    Reload the high scores from the JSON file.
    This function should be called before displaying or updating high scores.
    """
    load_high_scores()

# global instance of GameSettings
game_settings: GameSettings = GameSettings()

# more global variables
score: int = 0
high_scores: List[Tuple[str, int]] = []

# Load high scores when the module is imported
load_high_scores()
