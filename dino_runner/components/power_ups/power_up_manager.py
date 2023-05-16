import random
import pygame

from dino_runner.utils.constants import HEART_TYPE
from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.heart import Heart


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0
        self.power_up_type = 0

    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(200, 300)

            self.power_up_type = random.random()

            if self.power_up_type < 1/3:
                self.power_ups.append(Shield())
            elif self.power_up_type < 2/3: 
                self.power_ups.append(Hammer())
            else:
                self.power_ups.append(Heart())

    def update(self, game):
        self.generate_power_up(game.score)
        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)

            if game.player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                game.player.has_power_up = True
                game.player.type = power_up.type

                if power_up.type == HEART_TYPE:
                    game.sounds[2].play()
                    game.player.power_up_time = power_up.start_time + (30 * 1000)
                else:
                    game.player.power_up_time = power_up.start_time + (power_up.duration * 1000)

                self.power_ups.remove(power_up)


    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)