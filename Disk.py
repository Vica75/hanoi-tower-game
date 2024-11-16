import random

import pygame


class Disk:

    def __init__(self, stack_index, width_class):
        self.peg_index = 0
        self.stack_index = stack_index  # if 0 -> means bottom of the stack
        self.width_class = width_class  # if 0 -> means the smallest disk
        self.colour = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

    def move_up(self):
        pass
