import pygame

from GameState import GameState
from InputManager import InputManager
from Renderer import Renderer
import window_config

# define the window and the title
WIDTH, HEIGHT = window_config.WINDOW_WIDTH, window_config.WINDOW_HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hanoi Tower Solver", "icon")


def main():
    game_state = GameState()
    game_state.initialise_game(5)
    renderer = Renderer(game_state, WIN)
    input_manager = InputManager(game_state, renderer)

    running = True

    while running:
        renderer.draw_game()
        input_manager.handle_events()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
