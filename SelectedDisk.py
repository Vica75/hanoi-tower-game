from enum import Enum
from window_config import WINDOW_HEIGHT
import Peg
from Disk import Disk


class SelectedDisk(Disk):
    peg_candidate: Peg.Peg

    MAX_SCREEN_HEIGHT = 300
    MOVEMENT_SPEED = 300

    class DiskState(Enum):
        IDLE = 0
        MOVING_UP = 1
        MOVING_DOWN = 2
        MOVING_LEFT = 3
        MOVING_RIGHT = 4
        WAITING_FOR_INPUT = 5

    def __init__(self, stack_index, width_class, initial_peg_candidate, colour, on_finished_moving_down):
        super().__init__(stack_index, width_class, peg_index=initial_peg_candidate.index)
        self.peg_candidate = initial_peg_candidate
        self.state = SelectedDisk.DiskState.IDLE
        self.colour = colour
        self.on_finished_moving_down = on_finished_moving_down

    def tick(self, delta_time):
        if self.state != SelectedDisk.DiskState.IDLE:
            if self.state == SelectedDisk.DiskState.MOVING_UP:
                self.move_up(delta_time)
            elif self.state == SelectedDisk.DiskState.MOVING_DOWN:
                self.move_down(delta_time)
            elif self.state == SelectedDisk.DiskState.MOVING_LEFT:
                self.move_left(delta_time)
            elif self.state == SelectedDisk.DiskState.MOVING_RIGHT:
                self.move_right(delta_time)

    def move_up(self, delta_time):
        if self.screen_pos[1] > SelectedDisk.MAX_SCREEN_HEIGHT:
            self.screen_pos = (self.screen_pos[0], self.screen_pos[1] - SelectedDisk.MOVEMENT_SPEED * delta_time)
        else:
            self.state = SelectedDisk.DiskState.WAITING_FOR_INPUT

    def move_down(self, delta_time):
        max_pos = WINDOW_HEIGHT - (1 + len(self.peg_candidate.get_disks())) * Disk.HEIGHT
        if self.screen_pos[1] < max_pos:
            self.screen_pos = (self.screen_pos[0], self.screen_pos[1] + SelectedDisk.MOVEMENT_SPEED * delta_time)
        else:
            self.state = SelectedDisk.DiskState.IDLE
            self.on_finished_moving_down()

    def move_left(self, delta_time):
        min_pos = (self.peg_candidate.screen_pos[0] + (Peg.Peg.WIDTH / 2)) - (self.width / 2)
        if self.screen_pos[0] > min_pos:
            self.screen_pos = (self.screen_pos[0] - SelectedDisk.MOVEMENT_SPEED * delta_time, self.screen_pos[1])
        else:
            self.state = SelectedDisk.DiskState.WAITING_FOR_INPUT

    def move_right(self, delta_time):
        max_pos = (self.peg_candidate.screen_pos[0] + (Peg.Peg.WIDTH / 2)) - (self.width / 2)
        if self.screen_pos[0] < max_pos:
            self.screen_pos = (self.screen_pos[0] + SelectedDisk.MOVEMENT_SPEED * delta_time, self.screen_pos[1])
        else:
            self.state = SelectedDisk.DiskState.WAITING_FOR_INPUT

    def set_state(self, state: DiskState):
        self.state = state

    def set_peg_candidate(self, peg):
        self.peg_candidate = peg
