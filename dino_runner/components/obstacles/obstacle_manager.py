import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import *


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        
        if len(self.obstacles) == 0:
            random_obstacle = random.randint(0, 1)    

            if random_obstacle == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS + LARGE_CACTUS))
            elif random_obstacle == 1:
                self.obstacles.append(Bird(BIRD))
                    
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)

            if game.player.mask.overlap(obstacle.mask,
                (obstacle.rect.x - game.player.dino_rect.x, 
                 obstacle.rect.y - game.player.dino_rect.y)):
                if not game.player.has_power_ups and game.lifes_left > 0:
                    game.lifes_left -= 1
                    self.obstacles.remove(obstacle)
                elif game.player.type == SHIELD_TYPE:
                    self.obstacles.remove(obstacle)
                    game.player.reset_dino_state()
                elif game.player.type == HAMMER_TYPE and isinstance(obstacle, Bird):
                    self.obstacles.remove(obstacle)
                elif game.player.type == HAMMER_TYPE and isinstance(obstacle, Cactus):
                    game.player.reset_dino_state()

                else:
                    pygame.time.delay(500)
                    game.playing = False
                    break


    def reset_obstacles(self):
        self.obstacles = []

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen) 