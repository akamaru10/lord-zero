import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.heart import Heart
from dino_runner.utils.constants import DEFAULT_TYPE


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0

    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            random_power_up = random.randint(0,1)
            self.when_appears += random.randint(200, 300)
            if random_power_up == 0:
                self.power_ups.append(Shield())
            elif random_power_up == 1:
                self.power_ups.append(Hammer())

    def generate_extra_life(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(200, 300)
            self.power_ups.append(Heart())
                
    def update(self, game):
        if random.randint(0,2) == 0 and game.lifes_left < 3:
            self.generate_extra_life(game.score)
        else:
          self.generate_power_up(game.score)

        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)

            if game.player.mask.overlap(power_up.mask, (power_up.rect.x - game.player.dino_rect.x, power_up.rect.y - game.player.dino_rect.y)):
                if game.player.type == DEFAULT_TYPE and isinstance(power_up, Heart):
                    game.player.extra_life = True
                    game.lifes_left += 1
                power_up.start_time = pygame.time.get_ticks()
                game.player.shield = True
                game.player.has_power_ups = True
                game.player.type = power_up.type
                game.player.power_up_time = power_up.start_time + (power_up.duration * 1000)

                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)