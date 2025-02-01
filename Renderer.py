import pygame

from Disk import Disk
from GameState import GameState
import window_config
from GameView import GameView
from Peg import Peg


class Renderer:
    selected_disk_position: 'tuple(int, int)'

    # use config file to be able to reuse the window width and height in multiple files
    WINDOW_WIDTH = window_config.WINDOW_WIDTH
    WINDOW_HEIGHT = window_config.WINDOW_HEIGHT

    # background image
    BG = pygame.transform.scale(pygame.image.load("images/bg.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT))

    # selected disk movement animation properties
    MOVEMENT_SPEED = 200  # 200 px/s
    MAX_HEIGHT = 250

    def __init__(self, game_state: 'GameState', screen: 'pygame.Surface'):
        self.game_state = game_state
        self.screen = screen
        # current position of the selected disk - not yet selected at the initialisation stage
        self.selected_disk_position = None
        # define the clock for delta_time calculation
        self.clock = pygame.time.Clock()
        self.pegs_positions = []

    def draw(self):
        match self.game_state.current_screen:
            case GameView.START_SCREEN:
                self.draw_start_screen()
            case GameView.GAME_SCREEN:
                self.draw_game()
            case GameView.WIN_SCREEN:
                self.draw_win_screen()

    # drawing the start screen
    def draw_start_screen(self):
        self.draw_background()

    # drawing the win screen
    def draw_win_screen(self):
        self.draw_background()

    def draw_game(self):
        # draw background
        self.draw_background()

        # draw pegs
        for peg in self.game_state.get_pegs():
            self.draw_peg(peg)

        # draw disks
        for peg in self.game_state.get_pegs():
            for disk in peg.get_disks():
                self.draw_disk(disk)

        # draw selected disk
        if self.game_state.selected_disk:
            self.draw_disk(self.game_state.selected_disk)

    def draw_background(self):
        self.screen.blit(self.BG, (0, 0))

    def draw_peg(self, peg):
        # create a rectangle based on the peg dimensions
        peg_surface = pygame.Surface((Peg.WIDTH, Peg.HEIGHT))
        peg_surface.fill(Peg.COLOR)
        # draw the peg on the screen at the correct position
        self.screen.blit(peg_surface, peg.screen_pos)

    def draw_disk(self, disk):
        # create a rectangle based on the disk dimensions
        disk_surface = pygame.Surface((disk.width, Disk.HEIGHT))
        disk_surface.fill(disk.colour)
        # draw the rectangle at the correct position
        self.screen.blit(disk_surface, disk.screen_pos)
