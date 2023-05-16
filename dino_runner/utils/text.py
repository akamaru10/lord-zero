import pygame
from enum import Enum

class FontEnum(Enum):
    DEFAULT_FONT = ("freesansbold.ttf", 22)
    JURASSIC_FONT = ("./jurassic_park.ttf", 60)


def draw_text(game, texto, x_pos, y_pos, font: FontEnum = FontEnum.DEFAULT_FONT):
        font = pygame.font.Font(font.value[0], font.value[1])
        text = font.render(texto, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (x_pos, y_pos)
        game.screen.blit (text, text_rect)