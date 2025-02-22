import pygame
import os

from pygame import Surface


class AssetLoader:
    def __init__(self):
        self.assets = {}

    def load_image(self, name):
        # load the image
        path = os.path.join("images", name)
        image = pygame.image.load(path)

        # to preserve transparency
        image = image.convert_alpha()

        self.assets[name] = image
        return image

    def get_image(self, name):
        return self.assets[name]

    @staticmethod
    def scale_image(image: Surface, multiplier):
        return pygame.transform.scale(image, (image.get_width() * multiplier, image.get_height() * multiplier))
