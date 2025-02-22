import pygame.time
from Disk import Disk
from GameView import GameView
from Peg import Peg
from SelectedDisk import SelectedDisk


class GameState:
    # add type hints
    pegs: list[Peg]
    selected_disk: SelectedDisk | None
    clock = pygame.time.Clock()

    def __init__(self, current_screen):
        self.current_screen = current_screen
        self.pegs = []
        # current_disk - the disk that was selected to be moved in the current turn
        self.selected_disk = None
        self.selected_disk_move_direction = (0, 0)
        self.is_disk_moving = False
        self.number_of_disks = 0  # initialised in self.initialise_game()

    def initialise_game(self, number_of_disks):  # add number of pegs parameter
        # store the number of disks
        self.number_of_disks = number_of_disks

        # create the pegs
        for i in range(3):
            self.pegs.append(Peg(i))

        # add disks to the first peg
        for i in range(number_of_disks):
            disk = Disk(i, number_of_disks - i - 1)
            self.pegs[0].add_disk(disk)

    def set_current_screen(self, new_screen):
        self.current_screen = new_screen

    def tick(self):
        delta_time = GameState.clock.tick(60) / 1000.0
        if self.selected_disk:
            self.selected_disk.tick(delta_time)

    def get_pegs(self):
        return self.pegs
    
    def get_peg(self, index):
        return self.pegs[index]

    def set_selected_disk(self, disk: 'Disk | None'):
        if disk:
            self.selected_disk = SelectedDisk(
                disk.stack_index,
                disk.width_class,
                self.pegs[disk.peg_index],
                disk.colour,
                self.add_selected_disk_to_peg
            )
            self.selected_disk.set_state(SelectedDisk.DiskState.MOVING_UP)

    def add_selected_disk_to_peg(self):
        stack_index = len(self.selected_disk.peg_candidate.disks)
        width_class = self.selected_disk.width_class
        colour = self.selected_disk.colour
        peg_index = self.selected_disk.peg_candidate.index
        self.selected_disk.peg_candidate.add_disk(Disk(stack_index, width_class, colour, peg_index))
        self.selected_disk = None
        self.check_game_won()

    def check_game_won(self):
        # the peg that all the disks should be moved to in order to win the game
        win_peg = self.pegs[len(self.pegs)-1]

        # if all the disks are on the winning peg -> game won
        if len(win_peg.disks) == self.number_of_disks:
            print("Game Won!")
            self.current_screen = GameView.WIN_SCREEN
            return True
        else:
            print("Keep Playing!")
            return False

    def move_selected_disk_down(self):
        top_disk = self.selected_disk.peg_candidate.get_top_disk()
        # if the top disk is bigger than the selected disk or the peg is empty (top_disk is null)
        if top_disk and top_disk.width_class > self.selected_disk.width_class or (not top_disk):
            self.selected_disk.set_state(SelectedDisk.DiskState.MOVING_DOWN)

    def move_selected_disk_left(self):
        # check if the current peg candidate is not the leftmost one
        if self.selected_disk.peg_candidate.index > 0:
            # set the state and the new peg candidate
            self.selected_disk.set_state(SelectedDisk.DiskState.MOVING_LEFT)
            self.selected_disk.set_peg_candidate(self.pegs[self.selected_disk.peg_candidate.index - 1])

    def move_selected_disk_right(self):
        # check if the current peg candidate is not the rightmost one
        if self.selected_disk.peg_candidate.index < len(self.pegs) - 1:
            # set the state and the new peg candidate
            self.selected_disk.set_state(SelectedDisk.DiskState.MOVING_RIGHT)
            self.selected_disk.set_peg_candidate(self.pegs[self.selected_disk.peg_candidate.index + 1])
