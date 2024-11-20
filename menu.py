"""
This module handles the game initialization and settings.
It imports necessary libraries and constants, and sets up the game states and screen dimensions.
"""
from typing import (List, Tuple, Optional)
import sys
import pygame
from game import add_high_score
from settings import (WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, STATE_HIGH_SCORES, 
                      STATE_INSTRUCTIONS, STATE_OPTIONS, load_high_scores, 
                      high_scores, game_settings, DIFFICULTY_EASY, 
                      DIFFICULTY_HARD, DIFFICULTY_MEDIUM, COLOR_SCHEMES) 

menu_items: List[str] = ["Play", "High Scores", "Instructions", "Options", "Quit"]
menu_buttons: List[Tuple[pygame.Surface, pygame.Rect]] = []
start_game_callback: Optional[callable] = None

def setup_menu(start_game_func: callable) -> None:
    """
    Set up the main menu with buttons.
    Args:
        start_game_func (callable): Function to call when the play button is clicked.
    """
    global start_game_callback, menu_buttons
    start_game_callback = start_game_func
    font = pygame.font.Font(None, 36)
    for i, item in enumerate(menu_items):
        text = font.render(item, True, WHITE)
        button_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 70))
        menu_buttons.append((text, button_rect))

def show_menu(screen: pygame.Surface) -> None:
    """
    Display the main menu on the screen.
    Args:
        screen (pygame.Surface): The game screen surface.
    """
    for text, rect in menu_buttons:
        pygame.draw.rect(screen, WHITE, rect.inflate(20, 10), 2)
        screen.blit(text, rect)

def button_click(x: int, y: int) -> Optional[str]:
    """
    Handle button clicks in the main menu.
    Args:
        x (int): X-coordinate of the mouse click.
        y (int): Y-coordinate of the mouse click.
    Returns:
        Optional[str]: The new game state if a button was clicked, None otherwise.
    """
    for i, (_, rect) in enumerate(menu_buttons):
        if rect.collidepoint(x, y):
            if i == 0:  # Play
                if start_game_callback:
                    start_game_callback()
            elif i == 1:  # High Scores
                return STATE_HIGH_SCORES
            elif i == 2:  # Instructions
                return STATE_INSTRUCTIONS
            elif i == 3:  # Options
                return STATE_OPTIONS
            elif i == 4:  # Quit
                pygame.quit()
                sys.exit()
    return None

def show_instructions(screen: pygame.Surface) -> None:
    """
    Display the instructions screen.
    Args:
        screen (pygame.Surface): The game screen surface.
    """
    font = pygame.font.Font(None, 36)
    title = font.render("Instructions", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
    
    instructions = [
        "Use WASD keys to move the snake",
        "Eat food to grow and earn points",
        "Avoid hitting the walls or yourself",
        "POWER-UPS",
        "Square = Multiplier Boost",
        "Triangle = Speed Boost",
        "Circle = Invincibility"
    ]
    
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 150 + i * 50))
    
    back_text = font.render("Press M to return to menu", True, WHITE)
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 50))

def show_control_options(screen: pygame.Surface) -> List[Tuple[pygame.Rect, str]]:
    """
    Display the control options screen.
    Args:
        screen (pygame.Surface): The game screen surface.
    Returns:
        List[Tuple[pygame.Rect, str]]: List of control button rectangles and their associated actions.
    """
    font = pygame.font.Font(None, 36)
    title = font.render("Control Options", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

    controls = [('Up', 'up'), ('Down', 'down'), ('Left', 'left'), ('Right', 'right')]
    buttons = []

    for i, (control_name, control_key) in enumerate(controls):
        y_pos = 150 + i * 70
        text = font.render(f"{control_name}: {pygame.key.name(game_settings.controls[control_key])}", True, WHITE)
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, y_pos, 200, 40)
        pygame.draw.rect(screen, WHITE, button_rect, 2)
        screen.blit(text, (button_rect.x + 10, button_rect.y + 10))
        buttons.append((button_rect, control_key))

    back_text = font.render("Press M to return to options", True, WHITE)
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 50))

    return buttons

def show_options(screen: pygame.Surface) -> Optional[str]:
    """
    Display the options screen.
    Args:
        screen (pygame.Surface): The game screen surface.
    Returns:
        Optional[str]: The new game state if a button was clicked, None otherwise.
    """
    font = pygame.font.Font(None, 36)
    title = font.render("Options", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))

    # Difficulty options
    difficulty_text = font.render(f"Difficulty: {game_settings.difficulty}", True, WHITE)
    screen.blit(difficulty_text, (SCREEN_WIDTH // 2 - difficulty_text.get_width() // 2, 80))
    
    button_width, button_height = 200, 40
    easy_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 120, button_width, button_height)
    medium_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 170, button_width, button_height)
    hard_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 220, button_width, button_height)
    
    pygame.draw.rect(screen, WHITE, easy_button, 2)
    pygame.draw.rect(screen, WHITE, medium_button, 2)
    pygame.draw.rect(screen, WHITE, hard_button, 2)
    
    easy_text = font.render("Easy", True, WHITE)
    medium_text = font.render("Medium", True, WHITE)
    hard_text = font.render("Hard", True, WHITE)
    
    screen.blit(easy_text, (easy_button.centerx - easy_text.get_width() // 2, easy_button.centery - easy_text.get_height() // 2))
    screen.blit(medium_text, (medium_button.centerx - medium_text.get_width() // 2, medium_button.centery - medium_text.get_height() // 2))
    screen.blit(hard_text, (hard_button.centerx - hard_text.get_width() // 2, hard_button.centery - hard_text.get_height() // 2))

    # Color scheme options
    color_text = font.render(f"Color Scheme: {game_settings.color_scheme}", True, WHITE)
    screen.blit(color_text, (SCREEN_WIDTH // 2 - color_text.get_width() // 2, 280))
    
    default_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 320, 100, button_height)
    mono_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, 320, 100, button_height)
    neon_button = pygame.Rect(SCREEN_WIDTH // 2 + 50, 320, 100, button_height)
    
    pygame.draw.rect(screen, WHITE, default_button, 2)
    pygame.draw.rect(screen, WHITE, mono_button, 2)
    pygame.draw.rect(screen, WHITE, neon_button, 2)
    
    default_text = font.render("Default", True, WHITE)
    mono_text = font.render("Mono", True, WHITE)
    neon_text = font.render("Neon", True, WHITE)
    
    screen.blit(default_text, (default_button.centerx - default_text.get_width() // 2, default_button.centery - default_text.get_height() // 2))
    screen.blit(mono_text, (mono_button.centerx - mono_text.get_width() // 2, mono_button.centery - mono_text.get_height() // 2))
    screen.blit(neon_text, (neon_button.centerx - neon_text.get_width() // 2, neon_button.centery - neon_text.get_height() // 2))

    # Power-up toggle
    powerup_text = font.render(f"Power-ups: {'On' if game_settings.powerups_enabled else 'Off'}", True, WHITE)
    screen.blit(powerup_text, (SCREEN_WIDTH // 2 - powerup_text.get_width() // 2, 380))
    
    powerup_toggle_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 420, 300, button_height)
    pygame.draw.rect(screen, WHITE, powerup_toggle_button, 2)
    toggle_text = font.render("Toggle Power-ups", True, WHITE)
    screen.blit(toggle_text, (powerup_toggle_button.centerx - toggle_text.get_width() // 2, powerup_toggle_button.centery - toggle_text.get_height() // 2))

    # Control customization button
    control_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 480, 300, button_height)
    pygame.draw.rect(screen, WHITE, control_button, 2)
    control_text = font.render("Customize Controls", True, WHITE)
    screen.blit(control_text, (control_button.centerx - control_text.get_width() // 2, control_button.centery - control_text.get_height() // 2))

    back_text = font.render("Press M to return to menu", True, WHITE)
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 30))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if easy_button.collidepoint(mouse_pos):
                game_settings.set_difficulty(DIFFICULTY_EASY)
            elif medium_button.collidepoint(mouse_pos):
                game_settings.set_difficulty(DIFFICULTY_MEDIUM)
            elif hard_button.collidepoint(mouse_pos):
                game_settings.set_difficulty(DIFFICULTY_HARD)
            elif default_button.collidepoint(mouse_pos):
                game_settings.set_color_scheme('Default')
            elif mono_button.collidepoint(mouse_pos):
                game_settings.set_color_scheme('Monochrome')
            elif neon_button.collidepoint(mouse_pos):
                game_settings.set_color_scheme('Neon')
            elif powerup_toggle_button.collidepoint(mouse_pos):
                game_settings.toggle_powerups()
            elif control_button.collidepoint(mouse_pos):
                return "control_options"

    return None

def customize_controls(screen: pygame.Surface) -> None:
    """
    Display the control customization screen and handle user input for changing controls.

    This function allows the user to customize the game controls by clicking on a control
    button and then pressing a new key to assign to that control.

    Args:
        screen (pygame.Surface): The game screen surface to draw on.

    Returns:
        None

    Note:
        - The function runs in a loop until the user presses 'M' to return to the options menu.
        - It uses the show_control_options function to display the current control settings.
        - When a control is being changed, it displays a "Press a key..." message.
    """
    waiting_for_key = False
    current_control = None
    buttons = show_control_options(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return
                if waiting_for_key:
                    game_settings.set_control(current_control, event.key)
                    waiting_for_key = False
                    buttons = show_control_options(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN and not waiting_for_key:
                mouse_pos = event.pos
                for button, control in buttons:
                    if button.collidepoint(mouse_pos):
                        waiting_for_key = True
                        current_control = control

        screen.fill(COLOR_SCHEMES[game_settings.color_scheme]['background'])  # Clear the screen...CLEAR IT NOW
        buttons = show_control_options(screen)

        if waiting_for_key:
            font = pygame.font.Font(None, 36)
            text = font.render("Press a key...", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - 100))

        pygame.display.flip()

def show_high_scores(screen: pygame.Surface) -> None:
    """
    Display the high scores screen.
    Args:
        screen (pygame.Surface): The game screen surface.
    """
    load_high_scores()  # Load the most recent high scores (Or try to at least)
    print(f"Displaying high scores: {high_scores}")

    font = pygame.font.Font(None, 36)
    title = font.render("High Scores", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

    if not high_scores:
        no_scores_text = font.render("No high scores yet!", True, WHITE)
        screen.blit(no_scores_text, (SCREEN_WIDTH // 2 - no_scores_text.get_width() // 2, SCREEN_HEIGHT // 2))
    else:
        for i, (name, score) in enumerate(high_scores):
            score_text = font.render(f"{i+1}. {name}: {score}", True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 150 + i * 40))

    back_text = font.render("Press M to return to menu", True, WHITE)
    screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, SCREEN_HEIGHT - 50))

    pygame.display.flip()

    # Wait for 'M' key press to return to menu (WAAAAIIITTTTIIINNNNNG)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    waiting = False
                    break

def get_player_name(screen: pygame.Surface, score: int) -> None:
    """
    Display an input box for the player to enter their name for a high score.

    Args:
        screen (pygame.Surface): The game screen surface.
        score (int): The score achieved by the player.
    """
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 16, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        add_high_score(text, score)
                        print(f"Saving high score: {text} - {score}")  # Debug print
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(COLOR_SCHEMES[game_settings.color_scheme]['background'])
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        prompt_text = font.render("New High Score! Enter your name:", True, WHITE)
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

        pygame.display.flip()

    # After getting the player's name, update the high scores display
    show_high_scores(screen)
    pygame.time.wait(2000)  # Show the updated high scores for 2 seconds

__all__ = ['setup_menu', 'show_menu', 'button_click', 'show_high_scores', 
           'show_instructions', 'show_options', 'customize_controls']
