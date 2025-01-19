import pygame

from Disk import Disk
from GameState import GameState
import window_config
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

        # could move that logic into the peg class but the peg position is only calculated once and never changes
        for peg in self.game_state.get_pegs():
            # 3 pegs divide the screen into 4 areas, hence splitting the WINDOW_WIDTH by 4
            peg.screen_pos = (self.WINDOW_WIDTH / 4 * (peg.index + 1) - Peg.WIDTH / 2,
                              self.WINDOW_HEIGHT - Peg.HEIGHT)

    def draw_game(self):
        # calculate delta_time
        # delta_time = self.clock.tick(60) / 1000

        # print(self.game_state.is_disk_moving)
        # draw background
        self.draw_background()

        # draw pegs
        for peg in self.game_state.get_pegs():
            self.draw_peg(peg)

        # draw disks
        for peg in self.game_state.get_pegs():
            for disk in peg.get_disks():
                self.draw_disk(disk)

        # update position and draw the selected disk
        # if self.game_state.selected_disk:
        #     can_move_up = (
        #         self.game_state.selected_disk_move_direction == (0, -1)
        #         and self.selected_disk_position[1] > self.MAX_HEIGHT
        #     )
        #     can_move_down = (
        #         self.game_state.selected_disk_move_direction == (0, 1) and self.game_state.validate_move_down()
        #         and self.selected_disk_position[1]
        #         < self.WINDOW_HEIGHT - 50 - len(self.game_state.get_current_peg_candidate().disks) * self.DISK_HEIGHT
        #     )
        #     can_move_left = (
        #         self.game_state.selected_disk_move_direction == (-1, 0)
        #         and self.selected_disk_position[0] + (self.game_state.selected_disk.calculate_disk_width() / 2)
        #         > self.game_state.get_current_peg_candidate().screen_pos[0]
        #     )
        #     can_move_right = (
        #         self.game_state.selected_disk_move_direction == (1, 0)
        #         and self.selected_disk_position[0] + self.game_state.selected_disk.calculate_disk_width() / 2
        #         < self.game_state.get_current_peg_candidate().screen_pos[0]
        #     )
        #
        #     if can_move_up or can_move_down or can_move_right or can_move_left:
        #         self.update_selected_disk_position(delta_time)
        #     else:
        #         self.game_state.is_disk_moving = False
        #
        #     # self.draw_disk()

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

    # ----------- Selected Disk Movement --------------
    def set_selected_disk_base_position(self):
        self.selected_disk_position = self.game_state.selected_disk.calculate_screen_position()

    def update_selected_disk_position(self, delta_time):
        current_x, current_y = self.selected_disk_position
        offset_x = self.game_state.selected_disk_move_direction[0] * delta_time * self.MOVEMENT_SPEED
        offset_y = self.game_state.selected_disk_move_direction[1] * delta_time * self.MOVEMENT_SPEED
        self.selected_disk_position = (current_x + offset_x, current_y + offset_y)
