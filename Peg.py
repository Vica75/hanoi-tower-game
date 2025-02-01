from Disk import Disk
from window_config import WINDOW_WIDTH, WINDOW_HEIGHT


class Peg:
    WIDTH = 20
    HEIGHT = 300
    COLOR = (69, 39, 17)

    # TODO: refactor so that the screen position is assigned to the peg on initialisation
    # it is assigned to it anyway when the Renderer is initialised but it feels unclear
    def __init__(self, index):
        self.disks = []
        self.index = index
        # 3 pegs divide the screen into 4 areas, hence splitting the WINDOW_WIDTH by 4
        self.screen_pos = (WINDOW_WIDTH / 4 * (self.index + 1) - Peg.WIDTH / 2, WINDOW_HEIGHT - Peg.HEIGHT)

    def add_disk(self, disk: 'Disk'):
        self.disks.append(disk)

    def pop_disk(self):
        if self.disks:
            disk = self.disks.pop()
            return disk

    def get_top_disk(self) -> Disk | None:
        if self.disks:
            return self.disks[-1]
        else:
            return None

    def get_disk(self, index):
        return self.disks[index]

    def get_disks(self):
        return self.disks
