from Disk import Disk
from window_config import WINDOW_WIDTH, WINDOW_HEIGHT


class Peg:
    WIDTH = 20
    HEIGHT = 300
    COLOR = (69, 39, 17)

    def __init__(self, index):
        self.disks = []
        self.index = index
        self.screen_pos = ()

    def add_disk(self, disk: 'Disk'):
        self.disks.append(disk)

    def pop_disk(self):
        if self.disks:
            disk = self.disks.pop()
            print(disk.stack_index)
            return disk

    def get_top_disk(self):
        if self.disks:
            return self.disks[-1]
        else:
            return None

    def get_disk(self, index):
        return self.disks[index]

    def get_disks(self):
        return self.disks



