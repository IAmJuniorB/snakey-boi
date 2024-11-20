"""
This module manages the game logic and settings for the Snake game.
It imports necessary libraries and constants, and sets up the game modes, screen dimensions, colors, and power-ups.
"""
from typing import Tuple, List, Optional
import sys
import time
import random
import pygame
from settings import (
    GAME_MODE_TIME_ATTACK, SNAKE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,
    WHITE, BLACK, RED, GREEN, game_settings, high_scores, COLOR_SCHEMES,
    POWERUP_SPEED, POWERUP_MULTIPLIER, POWERUP_INVINCIBILITY, POWERUP_COLORS,
    POWERUP_DURATION, POWERUP_SPAWN_INTERVAL, POWERUP_SHAPES, save_high_scores, load_high_scores
)


snake: List[Tuple[int, int]] = []
food: Optional[Tuple[int, int]] = None
direction: Tuple[int, int] = (SNAKE_SIZE, 0)
last_move_time: int = 0
start_time: float = 0
time_left: int = 0
score: int = 0
powerup: Optional[Tuple[Tuple[int, int], str]] = None
active_powerups: dict = {}
last_powerup_spawn: int = 0

wall_group = pygame.sprite.Group()

class Wall(pygame.sprite.Sprite):
    """Represents a wall in the game."""

    def __init__(self, x: int, y: int):
        """
        Initialize a wall sprite.
        Args:
            x (int): The x-coordinate of the wall.
            y (int): The y-coordinate of the wall.
        """
        super().__init__()
        self.rect = pygame.Rect(x, y, SNAKE_SIZE, SNAKE_SIZE)

def game_loop(screen: pygame.Surface) -> Tuple[str, int]:
    """
    Main game loop function.
    Args:
        screen (pygame.Surface): The game screen surface.
    Returns:
        Tuple[str, int]: The game state after the loop and the final score.
    """
    global snake, food, powerup, direction, score, current_state, last_move_time, start_time, time_left, last_powerup_spawn, active_powerups

    current_time = pygame.time.get_ticks()

    if game_settings.game_mode == GAME_MODE_TIME_ATTACK and start_time == 0:
        start_time = time.time()

    # Spawn power-up
    if game_settings.powerups_enabled and current_time - last_powerup_spawn > POWERUP_SPAWN_INTERVAL * 1000:
        if powerup is None:
            place_powerup()
        last_powerup_spawn = current_time

    # Update active power-ups
    for powerup_type in list(active_powerups.keys()):
        if current_time - active_powerups[powerup_type] > POWERUP_DURATION[powerup_type] * 1000:
            del active_powerups[powerup_type]

    # Adjust snake speed for snakey boi boooooost
    current_speed = game_settings.snake_speed
    if POWERUP_SPEED in active_powerups:
        current_speed //= 2

    if current_time - last_move_time > current_speed:
        last_move_time = current_time

        # Calculate new head position (Not that head)
        new_head = (
            snake[0][0] + direction[0],
            snake[0][1] + direction[1]
        )

        # Check for collision with walls or self (Unless you are invincible and get lost in the ether)
        collision = (
            any(wall.rect.collidepoint(new_head) for wall in wall_group) or
            new_head in snake[1:]
        )
        
        if collision and POWERUP_INVINCIBILITY not in active_powerups:
            return game_over(screen), score

        # Move the snake
        snake.insert(0, new_head)
        if new_head == food:
            score_increase = 1
            if POWERUP_MULTIPLIER in active_powerups:
                score_increase *= 2
            score += score_increase
            food = place_food()
        elif powerup and new_head == powerup[0]:
            active_powerups[powerup[1]] = current_time
            powerup = None
        else:
            snake.pop()

    # Draw
    colors = COLOR_SCHEMES[game_settings.color_scheme]
    screen.fill(colors['background'])
    for wall in wall_group:
        pygame.draw.rect(screen, WHITE, wall.rect)
    for segment in snake:
        pygame.draw.rect(screen, colors['snake'], (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
    pygame.draw.rect(screen, colors['food'], (food[0], food[1], SNAKE_SIZE, SNAKE_SIZE))
    
    # Draw power-up
    if powerup:
        powerup_pos, powerup_type = powerup
        powerup_shape = POWERUP_SHAPES[powerup_type]
        powerup_color = POWERUP_COLORS[powerup_type]
        
        if powerup_shape == "triangle":
            points = [
                (powerup_pos[0], powerup_pos[1] + SNAKE_SIZE),
                (powerup_pos[0] + SNAKE_SIZE, powerup_pos[1] + SNAKE_SIZE),
                (powerup_pos[0] + SNAKE_SIZE // 2, powerup_pos[1])
            ]
            pygame.draw.polygon(screen, powerup_color, points)
        elif powerup_shape == "square":
            pygame.draw.rect(screen, powerup_color, (*powerup_pos, SNAKE_SIZE, SNAKE_SIZE))
        elif powerup_shape == "circle":
            pygame.draw.circle(screen, powerup_color, (powerup_pos[0] + SNAKE_SIZE // 2, powerup_pos[1] + SNAKE_SIZE // 2), SNAKE_SIZE // 2)

    # Draw score, time, and active power-ups
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (SNAKE_SIZE + 5, SNAKE_SIZE + 5))

    if game_settings.game_mode == GAME_MODE_TIME_ATTACK:
        time_left = max(0, game_settings.time_attack_duration - int(time.time() - start_time))
        time_text = font.render(f"Time: {time_left}", True, WHITE)
        screen.blit(time_text, (SCREEN_WIDTH - 150, SNAKE_SIZE + 5))

        if time_left == 0:
            return game_over(screen), score

    # Draw active power-ups
    for i, powerup_type in enumerate(active_powerups):
        powerup_text = font.render(f"{powerup_type.capitalize()}", True, POWERUP_COLORS[powerup_type])
        screen.blit(powerup_text, (SNAKE_SIZE + 5, SNAKE_SIZE + 40 + i * 30))

    return "continue", score

def setup_game() -> None:
    """
    Set up the initial game state.
    """
    global snake, food, direction, wall_group, score, powerup, active_powerups, last_powerup_spawn
    snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
    food = place_food()
    direction = (SNAKE_SIZE, 0)
    score = 0
    powerup = None
    active_powerups = {}
    last_powerup_spawn = 0

    # Create walls
    wall_group.empty()  # Clear any existing walls. No backrooms for you.
    # Create border walls. But nothing like Trump.
    for x in range(0, SCREEN_WIDTH, SNAKE_SIZE):
        wall_group.add(Wall(x, 0))
        wall_group.add(Wall(x, SCREEN_HEIGHT - SNAKE_SIZE))
    for y in range(0, SCREEN_HEIGHT, SNAKE_SIZE):
        wall_group.add(Wall(0, y))
        wall_group.add(Wall(SCREEN_WIDTH - SNAKE_SIZE, y))

def place_item() -> Tuple[int, int]:
    """
    Place an item (food or powerup) on the game board.
    Returns:
        Tuple[int, int]: The (x, y) coordinates of the placed item.
    Note:
        This function ensures that the item is not placed on the snake or any wall.
    """
    while True:
        x = random.randint(1, (SCREEN_WIDTH // SNAKE_SIZE) - 2) * SNAKE_SIZE
        y = random.randint(1, (SCREEN_HEIGHT // SNAKE_SIZE) - 2) * SNAKE_SIZE
        item_pos = (x, y)
        if item_pos not in snake and not any(wall.rect.collidepoint(item_pos) for wall in wall_group):
            return item_pos

def place_food() -> Tuple[int, int]:
    """
    Place food on the game board.
    Returns:
        Tuple[int, int]: The (x, y) coordinates of the placed food.
    """
    return place_item()

def place_powerup() -> None:
    """
    Place a powerup on the game board.
    This function selects a random powerup type and places it on the board.
    The global 'powerup' variable is updated with the new powerup information.
    """
    global powerup
    powerup_type: str = random.choice([POWERUP_SPEED, POWERUP_MULTIPLIER, POWERUP_INVINCIBILITY])
    powerup = (place_item(), powerup_type)

def game_over(screen: pygame.Surface) -> str:
    """
    Handle the game over state.
    Args:
        screen (pygame.Surface): The game screen surface.
    Returns:
        str: The next game state ('play_again', 'main_menu', or 'new_high_score').
    """
    global current_state, score, high_scores, start_time, time_left
    font = pygame.font.Font(None, 72)
    text = font.render("GAME OVER", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    if game_settings.game_mode == GAME_MODE_TIME_ATTACK:
        final_time = game_settings.time_attack_duration - time_left
        time_text = font.render(f"Time: {final_time} seconds", True, WHITE)
        screen.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    
    play_again_text = font.render("Play Again?", True, WHITE)
    screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))
    
    yes_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200, 80, 40)
    no_button = pygame.Rect(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 200, 80, 40)
    
    pygame.draw.rect(screen, GREEN, yes_button)
    pygame.draw.rect(screen, RED, no_button)
    
    font = pygame.font.Font(None, 36)
    yes_text = font.render("Yes", True, BLACK)
    no_text = font.render("No", True, BLACK)
    
    screen.blit(yes_text, (yes_button.x + 20, yes_button.y + 10))
    screen.blit(no_text, (no_button.x + 25, no_button.y + 10))
    
    pygame.display.flip()
    
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if yes_button.collidepoint(mouse_pos):
                    reset_game()
                    return "play_again"
                elif no_button.collidepoint(mouse_pos):
                    if not high_scores or score > min(high_scores, key=lambda x: x[1])[1]:
                        return "new_high_score"
                    else:
                        return "main_menu"
    
    return "main_menu"  # Default to main menu if loop is somehow exited...Cuz, you know, things happen.

def reset_game() -> None:
    """
    Reset the game state for a new game.
    """
    global score, start_time, time_left
    score = 0
    start_time = 0
    if game_settings.game_mode == GAME_MODE_TIME_ATTACK:
        time_left = game_settings.time_attack_duration
    else:
        time_left = 0
    setup_game()

def handle_keys(event: pygame.event.Event) -> None:
    """
    Handle key press events to control the snake.
    Args:
        event (pygame.event.Event): The key press event.
    """
    global direction
    if event.key == game_settings.controls['up'] and direction != (0, SNAKE_SIZE):
        direction = (0, -SNAKE_SIZE)
    elif event.key == game_settings.controls['down'] and direction != (0, -SNAKE_SIZE):
        direction = (0, SNAKE_SIZE)
    elif event.key == game_settings.controls['left'] and direction != (SNAKE_SIZE, 0):
        direction = (-SNAKE_SIZE, 0)
    elif event.key == game_settings.controls['right'] and direction != (-SNAKE_SIZE, 0):
        direction = (SNAKE_SIZE, 0)

def add_high_score(name: str, score: int):
    """
    Add a new high score to the list, sort it, and save it to the file.

    Args:
        name (str): The name of the player.
        score (int): The score achieved by the player.
    """
    global high_scores
    high_scores = load_high_scores()  # Load existing high scores. This again...
    high_scores.append((name, score))
    high_scores.sort(key=lambda x: x[1], reverse=True)
    high_scores = high_scores[:5]  # Keep only top 5 scores...Or 1 really
    save_high_scores()
    print(f"Added high score: {name} - {score}")
    print(f"Updated high scores: {high_scores}")

__all__ = ['setup_game', 'game_loop', 'reset_game', 'handle_keys']
