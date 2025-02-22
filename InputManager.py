import pygame
import SelectedDisk
from GameState import GameState
from GameView import GameView
from Renderer import Renderer


class InputManager:
    def __init__(self, game_state: 'GameState', renderer: 'Renderer'):
        self.game_state = game_state
        self.renderer = renderer

    def handle_events(self):
        match self.game_state.current_screen:
            case GameView.START_SCREEN:
                self.handle_start_screen_events()
            case GameView.GAME_SCREEN:
                self.handle_game_events()
            case GameView.WIN_SCREEN:
                self.handle_win_screen_events()

    def handle_start_screen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # this will run only once, when the key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Enter Key Pressed")
                    self.game_state.set_current_screen(GameView.GAME_SCREEN)

    def handle_win_screen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()

    def handle_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # this will run only once, when the key is pressed
            elif event.type == pygame.KEYDOWN:
                # Handle the case when none of the disks is selected - wait for selection
                if not self.game_state.selected_disk:
                    if event.key == pygame.K_1:
                        # could be replaced by a function in GameState that only takes the peg index,
                        # but I find this more readable
                        self.game_state.set_selected_disk(self.game_state.get_peg(0).pop_disk())
                    elif event.key == pygame.K_2:
                        self.game_state.set_selected_disk(self.game_state.get_peg(1).pop_disk())
                    elif event.key == pygame.K_3:
                        self.game_state.set_selected_disk(self.game_state.get_peg(2).pop_disk())

                # Handle the case where one of the disks is already selected - handle its movement
                elif self.game_state.selected_disk.state == SelectedDisk.SelectedDisk.DiskState.WAITING_FOR_INPUT:
                    if event.key == pygame.K_LEFT:
                        self.game_state.move_selected_disk_left()
                    elif event.key == pygame.K_RIGHT:
                        self.game_state.move_selected_disk_right()
                    elif event.key == pygame.K_DOWN:
                        self.game_state.move_selected_disk_down()
