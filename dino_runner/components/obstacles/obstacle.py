import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_HEIGHT


class Obstacle(Sprite):
    def __init__(self, image):
        self.image = image
        self.typpe = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_HEIGHT

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed

        if self.rect.x < -self.rect_width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.typpe], (self.rect.x, self.rect.y))