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

# called to initialise all pygame modules that need it. Can be used instead of manually initialising every module
# that we may want to use e.g. pygame.display.init(), pygame.fonts.init() etc.
pygame.init()


def main():
    running = True
    current_view = GameView.START_SCREEN
    game_state = GameState(current_view)

    game_state.initialise_game(6)
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
