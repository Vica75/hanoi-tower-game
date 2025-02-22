import random
from window_config import WINDOW_WIDTH, WINDOW_HEIGHT


class Disk:

    # when used with pygame surface can be chosen. When used with actual sprites, can be calculated manually,
    # based on the sprite size, or guessed
    HEIGHT = 50  # mathematically, it should be 54 (9px multiplied by 6) but 50 looks visually better
    BASE_WIDTH = 96  # 16 (actual size of the box on the sprite) * 6 (scale value)
    EXTENSION_WIDTH = 18  # 3 * 6

    def __init__(self, stack_index, width_class, colour=None, peg_index=0):
        self.peg_index = peg_index
        self.stack_index = stack_index  # if 0 -> means bottom of the stack
        self.width_class = width_class  # if 0 -> means the smallest disk
        self.width = Disk.BASE_WIDTH + (self.width_class * Disk.EXTENSION_WIDTH)
        if colour:
            self.colour = colour
        else:
            self.colour = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
        self.screen_pos = self.calculate_screen_position()

    def set_position(self, position: tuple):
        self.screen_pos = position

    def calculate_screen_position(self):
        # calculate the x position based on the peg index, the width of the window and disk_width
        pos_x = (self.peg_index + 1) * (WINDOW_WIDTH / 4) - (self.width / 2)
        pos_y = WINDOW_HEIGHT - Disk.HEIGHT * (self.stack_index + 1)

        return pos_x, pos_y
