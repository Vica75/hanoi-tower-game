import pygame
from GameState import GameState
from GameView import GameView
from InputManager import InputManager
from Renderer import Renderer
import window_config

# define the window and the title
WIDTH, HEIGHT = window_config.WINDOW_WIDTH, window_config.WINDOW_HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hanoi Tower Solver", "icon")


def main():
    running = True
    current_view = GameView.GAME_SCREEN
    game_state = GameState(current_view)

    game_state.initialise_game(3)
    renderer = Renderer(game_state, WIN)
    input_manager = InputManager(game_state, renderer)

    while running:
        renderer.draw()
        input_manager.handle_events()
        game_state.tick()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
