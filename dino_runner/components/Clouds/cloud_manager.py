import pygame
import random

from dino_runner.components.clouds.cloud import Cloud
from dino_runner.utils.constants import SCREEN_HEIGHT


class Cloud:
    def __init__(self,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_HEIGHT

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, game_speed, clouds):
        self.rect.x -= game_speed

        if self.rect.x < -self.rect.width:
            clouds.pop()