"""
This module initializes the game settings and imports necessary libraries and constants.
It sets up the screen dimensions, game states, color schemes, and frame rate for the game.
"""
import sys
from typing import Optional
import pygame
from settings import (SCREEN_HEIGHT, SCREEN_WIDTH,STATE_MENU, STATE_GAME,
                      COLOR_SCHEMES, game_settings, STATE_HIGH_SCORES,
                      STATE_INSTRUCTIONS, STATE_OPTIONS, FPS)
from menu import (setup_menu, show_menu, button_click, show_high_scores, 
                  show_instructions, show_options, customize_controls, 
                  get_player_name, load_high_scores)
from game import (setup_game, game_loop, reset_game, handle_keys)

# Initialize
pygame.init()

# Set up screen
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snakey Boi")

# Initialize game state
current_state: str = STATE_MENU

def start_game() -> None:
    """
    Start a new game by resetting the game state and changing to the game screen.
    """
    global current_state
    print("start_game function called")
    current_state = STATE_GAME
    reset_game()

setup_menu(start_game)
setup_game()

# Main game loop
clock: pygame.time.Clock = pygame.time.Clock()

def main_loop() -> None:
    """
    The main game loop that handles events, updates game state, and renders the screen.
    """
    load_high_scores()  # Load high scores at the start of the program as I was, and still are, experiencing issues with it
    global current_state, score
    score = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and current_state == STATE_MENU:
                new_state: Optional[str] = button_click(event.pos[0], event.pos[1])
                if new_state:
                    current_state = new_state
            elif event.type == pygame.KEYDOWN:
                if current_state == STATE_GAME:
                    handle_keys(event)
                elif event.key == pygame.K_m and current_state != STATE_MENU:
                    current_state = STATE_MENU

        colors: dict = COLOR_SCHEMES[game_settings.color_scheme]
        screen.fill(colors['background'])

        if current_state == STATE_MENU:
            show_menu(screen)
        elif current_state == STATE_GAME:
            game_result, score = game_loop(screen)
            if game_result == "new_high_score":
                get_player_name(screen, score)
                current_state = STATE_MENU
            elif game_result == "main_menu":
                current_state = STATE_MENU
            elif game_result == "play_again":
                reset_game()
                score = 0  # Reset score
        elif current_state == STATE_HIGH_SCORES:
            show_high_scores(screen)
            current_state = STATE_MENU
        elif current_state == STATE_INSTRUCTIONS:
            show_instructions(screen)
        elif current_state == STATE_OPTIONS:
            option_result: Optional[str] = show_options(screen)
            if option_result == "control_options":
                current_state = "control_options"
        elif current_state == "control_options":
            customize_controls(screen)
            current_state = STATE_OPTIONS

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    load_high_scores()
    main_loop()
