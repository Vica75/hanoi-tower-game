import pygame

from Disk import Disk
from GameState import GameState
import window_config


class Renderer:
    selected_disk_position: 'tuple(int, int)'

    # use config file to be able to reuse the window width and height in multiple files
    WINDOW_WIDTH = window_config.WINDOW_WIDTH
    WINDOW_HEIGHT = window_config.WINDOW_HEIGHT

    # background image
    BG = pygame.transform.scale(pygame.image.load("images/bg.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT))

    # disk and peg visual properties
    DISK_HEIGHT = 40
    DISK_BASE_WIDTH = 60
    DISK_EXTENSION_WIDTH = 40
    PEG_WIDTH = 20
    PEG_HEIGHT = 300
    PEG_COLOR = (69, 39, 17)

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

        for peg in self.game_state.get_pegs():
            # 3 pegs divide the screen into 4 areas, hence splitting the WINDOW_WIDTH by 4
            peg.screen_pos = (self.WINDOW_WIDTH / 4 * (peg.index + 1) - self.PEG_WIDTH / 2,
                              self.WINDOW_HEIGHT - self.PEG_HEIGHT)

    def draw_game(self):
        # calculate delta_time
        delta_time = self.clock.tick(60) / 1000

        print(self.game_state.is_disk_moving)
        # draw background
        self.draw_background()

        # draw pegs
        for peg in self.game_state.get_pegs():
            self.draw_peg(peg)

        # draw disks
        for peg in self.game_state.get_pegs():
            for disk in peg.get_disks():
                self.draw_disk_old(disk)

        # update position and draw the selected disk
        if self.game_state.selected_disk:
            can_move_up = (
                self.game_state.selected_disk_move_direction == (0, -1)
                and self.selected_disk_position[1] > self.MAX_HEIGHT
            )
            can_move_down = (
                self.game_state.selected_disk_move_direction == (0, 1) and self.game_state.validate_move_down()
                and self.selected_disk_position[1]
                < self.WINDOW_HEIGHT - 50 - len(self.game_state.get_current_peg_candidate().disks) * self.DISK_HEIGHT
            )
            can_move_left = (
                self.game_state.selected_disk_move_direction == (-1, 0)
                and self.selected_disk_position[0] + (self.calculate_disk_width(self.game_state.selected_disk) / 2)
                > self.game_state.get_current_peg_candidate().screen_pos[0]
            )
            can_move_right = (
                self.game_state.selected_disk_move_direction == (1, 0)
                and self.selected_disk_position[0] + self.calculate_disk_width(self.game_state.selected_disk) / 2
                < self.game_state.get_current_peg_candidate().screen_pos[0]
            )

            if can_move_up or can_move_down or can_move_right or can_move_left:
                self.update_selected_disk_position(delta_time)
            else:
                self.game_state.is_disk_moving = False

            self.draw_disk_old(self.game_state.selected_disk, self.selected_disk_position)

    def draw_background(self):
        self.screen.blit(self.BG, (0, 0))

    def draw_peg(self, peg):
        peg_surface = pygame.Surface((self.PEG_WIDTH, self.PEG_HEIGHT))
        peg_surface.fill(self.PEG_COLOR)
        self.screen.blit(peg_surface, peg.screen_pos)

    def draw_disk_old(self, disk: 'Disk', pos=None):

        disk_width = self.calculate_disk_width(disk)

        disk_surface = pygame.Surface((disk_width, self.DISK_HEIGHT))
        disk_surface.fill(disk.colour)

        # if the position is provided, draw at that position. If not, calculate it based on the peg and stack_index
        if pos:
            pos_x, pos_y = pos
        else:
            pos_x, pos_y = self.calculate_disk_position(disk)

        self.screen.blit(disk_surface, (pos_x, pos_y))

    def calculate_disk_width(self, disk: 'Disk'):
        # calculate the disk width based on the width class (size) and the constant variables
        return self.DISK_BASE_WIDTH + (disk.width_class * self.DISK_EXTENSION_WIDTH)

    def calculate_disk_position(self, disk: 'Disk'):
        disk_width = self.calculate_disk_width(disk)

        # calculate the x position based on the peg index, the width of the window and disk_width
        pos_x = (disk.peg_index + 1) * (self.WINDOW_WIDTH / 4) - (disk_width / 2)
        pos_y = self.WINDOW_HEIGHT - self.DISK_HEIGHT * (disk.stack_index + 1)

        return pos_x, pos_y

    # ----------- Selected Disk Movement --------------
    def set_selected_disk_base_position(self):
        self.selected_disk_position = self.calculate_disk_position(self.game_state.selected_disk)

    def update_selected_disk_position(self, delta_time):
        current_x, current_y = self.selected_disk_position
        offset_x = self.game_state.selected_disk_move_direction[0] * delta_time * self.MOVEMENT_SPEED
        offset_y = self.game_state.selected_disk_move_direction[1] * delta_time * self.MOVEMENT_SPEED
        self.selected_disk_position = (current_x + offset_x, current_y + offset_y)
