from enum import Enum

from Disk import Disk
from Peg import Peg


# class DiskMovementState(Enum):
#     NONE: 0
#     MOVING_UP: 1
#     MOVING_DOWN: 2
#     MOVING_HORIZONTALLY: 3


class GameState:
    # add type hints
    pegs: list[Peg]
    selected_disk: Disk | None
    # selected_disk_state: DiskMovementState
    current_peg_candidate_index: int

    def __init__(self):
        self.pegs = []
        # current_disk - the disk that was selected to be moved in the current turn
        self.selected_disk = None
        # self.selected_disk_state = DiskMovementState.NONE
        # set the peg candidate index to -1 meaning None
        self.current_peg_candidate_index = -1
        self.selected_disk_move_direction = (0, 0)
        self.is_disk_moving = False

    def initialise_game(self, number_of_disks):  # add number of pegs parameter
        # create the pegs
        for i in range(3):
            self.pegs.append(Peg(i))

        # add disks to the first peg
        for i in range(number_of_disks):
            disk = Disk(i, number_of_disks - i)
            self.pegs[0].add_disk(disk)

    def get_pegs(self):
        return self.pegs
    
    def get_peg(self, index):
        return self.pegs[index]

    def get_current_peg_candidate(self) -> Peg | None:
        if self.current_peg_candidate_index != -1:
            return self.pegs[self.current_peg_candidate_index]
        else:
            return None

    def set_selected_disk(self, disk: 'Disk | None'):
        if disk:
            self.selected_disk = disk
            # self.selected_disk_state = DiskMovementState.MOVING_UP
            # self.selected_disk_move_direction = (0, -1)
            self.current_peg_candidate_index = disk.peg_index

    def reset_selected_disk(self):
        self.selected_disk = None
        # self.selected_disk_state = DiskMovementState.NONE
        self.selected_disk_move_direction = (0, 0)
        self.current_peg_candidate_index = -1

    def set_selected_disk_move_direction(self, direction: 'tuple(int, int)'):
        self.selected_disk_move_direction = direction
        if direction == (1, 0) and self.current_peg_candidate_index < len(self.pegs) - 1:
            self.current_peg_candidate_index += 1
            self.is_disk_moving = True
        elif direction == (-1, 0) and self.current_peg_candidate_index > 0:
            self.current_peg_candidate_index -= 1
            self.is_disk_moving = True
        elif direction == (0, 1) or direction == (0, -1):
            self.is_disk_moving = True

    # check if the disk can be put on top of the candidate peg stack
    def validate_move_down(self):
        if (not self.get_current_peg_candidate().get_top_disk()
                or self.get_current_peg_candidate().get_top_disk().width_class > self.selected_disk.width_class):
            return True
        else:
            return False

    def move_selected_disk_down(self):
        if self.validate_move_down():
            self.get_current_peg_candidate().add_disk(self.selected_disk)
            self.reset_selected_disk()
