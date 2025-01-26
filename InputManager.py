import pygame

import SelectedDisk
from Disk import Disk
from GameState import GameState
from Renderer import Renderer


class InputManager:
    def __init__(self, game_state: 'GameState', renderer: 'Renderer'):
        self.game_state = game_state
        self.renderer = renderer

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # this will run only once, when the key is pressed
            elif event.type == pygame.KEYDOWN:
                if not self.game_state.selected_disk:
                    if event.key == pygame.K_1:
                        # could be replaced by a function in GameState that only takes the peg index,
                        # but I find this more readable
                        print("selecting disk")
                        self.game_state.set_selected_disk(self.game_state.get_peg(0).pop_disk())
                    elif event.key == pygame.K_2:
                        self.game_state.set_selected_disk(self.game_state.get_peg(1).pop_disk())
                        self.renderer.set_selected_disk_base_position()
                    elif event.key == pygame.K_3:
                        self.game_state.set_selected_disk(self.game_state.get_peg(2).pop_disk())
                        self.renderer.set_selected_disk_base_position()
                elif self.game_state.selected_disk.state == SelectedDisk.SelectedDisk.DiskState.WAITING_FOR_INPUT:
                    if event.key == pygame.K_LEFT:
                        if self.game_state.selected_disk:
                            self.game_state.set_selected_disk_move_direction((-1, 0))
                            # self.game_state.handle_move_disk
                    elif event.key == pygame.K_RIGHT:
                        if self.game_state.selected_disk:
                            self.game_state.set_selected_disk_move_direction((1, 0))
                    elif event.key == pygame.K_DOWN:
                        if self.game_state.selected_disk:
                            self.game_state.set_selected_disk_move_direction((0, 1))
