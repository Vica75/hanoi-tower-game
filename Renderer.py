import pygame

from AssetLoader import AssetLoader
from Disk import Disk
from GameState import GameState
import window_config
from GameView import GameView
from Peg import Peg


class Renderer:
    selected_disk_position: 'tuple(int, int)'

    # use config file to be able to reuse the window width and height in multiple files
    WINDOW_WIDTH = window_config.WINDOW_WIDTH
    WINDOW_HEIGHT = window_config.WINDOW_HEIGHT

    # background image
    BG = pygame.transform.scale(pygame.image.load("images/bg.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT))

    # menu fonts
    pygame.font.init()
    fonts = {
        'move_counter': pygame.font.Font('fonts/Goldman/Goldman-Regular.ttf', 96),
        'menu_big': pygame.font.Font('fonts/Goldman/Goldman-Bold.ttf', 96),
        'menu_small': pygame.font.SysFont('fonts/Goldman/Goldman-Regular.ttf', 44, True)
    }

    # menu text colour
    TEXT_COLOUR = (0, 0, 100)

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
        # array of box images
        self.box_images = Renderer.load_box_images()

    @staticmethod
    def load_box_images():
        loader = AssetLoader()
        boxes = []
        # add all "box_size_i.png" images to the box array
        for i in range(6):
            box = loader.load_image("box_size_" + str(i) + ".png")
            box = loader.scale_image(box, 6)
            boxes.append(box)

        return boxes

    def draw(self):
        match self.game_state.current_screen:
            case GameView.START_SCREEN:
                self.draw_start_screen()
            case GameView.GAME_SCREEN:
                self.draw_game()
            case GameView.WIN_SCREEN:
                self.draw_win_screen()

    # drawing the start screen
    def draw_start_screen(self):
        self.draw_background()
        # draw title text
        title_surface = Renderer.fonts['menu_big'].render(
            "Hanoi Tower",
            True,  # blur the edges to avoid jagged surface
            Renderer.TEXT_COLOUR
        )
        x_pos = self.WINDOW_WIDTH / 2 - title_surface.get_width() / 2
        self.screen.blit(title_surface, (x_pos, 200))

        # draw "enter to play" text
        play_surface = Renderer.fonts['menu_small'].render(
            "Press Enter to Play",
            True,  # blur the edges to avoid jagged surface
            Renderer.TEXT_COLOUR
        )
        x_pos = self.WINDOW_WIDTH / 2 - play_surface.get_width() / 2
        self.screen.blit(play_surface, (x_pos, 400))

    # drawing the win screen
    def draw_win_screen(self):
        self.draw_background()
        # draw "you won" text
        win_text_surface = Renderer.fonts['menu_big'].render(
            "You Won!",
            True,  # blur the edges to avoid jagged surface
            Renderer.TEXT_COLOUR
        )
        x_pos = self.WINDOW_WIDTH / 2 - win_text_surface.get_width() / 2
        self.screen.blit(win_text_surface, (x_pos, 200))


    def draw_game(self):
        # draw background
        self.draw_background()

        # draw number of moves text
        text_surface = Renderer.fonts['move_counter'].render(
            str(self.game_state.number_of_moves),
            True,  # blur the edges to avoid jagged surface
            Renderer.TEXT_COLOUR
        )
        x_pos = self.WINDOW_WIDTH/2 - text_surface.get_width()/2
        self.screen.blit(text_surface, (x_pos, 20))

        # draw pegs
        for peg in self.game_state.get_pegs():
            self.draw_peg(peg)

        # draw disks
        for peg in self.game_state.get_pegs():
            for disk in peg.get_disks():
                self.draw_disk(disk)

        # draw selected disk
        if self.game_state.selected_disk:
            self.draw_disk(self.game_state.selected_disk)

    def draw_background(self):
        self.screen.blit(self.BG, (0, 0))

    def draw_peg(self, peg):
        # create a rectangle based on the peg dimensions
        peg_surface = pygame.Surface((Peg.WIDTH, Peg.HEIGHT))
        peg_surface.fill(Peg.COLOR)
        # draw the peg on the screen at the correct position
        self.screen.blit(peg_surface, peg.screen_pos)

    def draw_disk(self, disk):
        # get the disk image
        disk_image = self.box_images[disk.width_class]
        # draw the rectangle at the correct position
        self.screen.blit(disk_image, disk.screen_pos)
