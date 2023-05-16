import pygame
import random

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, SHIELD_TYPE, HAMMER_TYPE, HEART_TYPE


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
    
    def update(self, game):
        if len(self.obstacles) == 0:
            if random.random() < 0.8:
                self.obstacles.append(Cactus((SMALL_CACTUS + LARGE_CACTUS)))
            else:
                self.obstacles.append(Bird())

        self.handle_colliderect(game)

    def handle_colliderect(self, game):
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    game.sounds[3].play()
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    self.obstacles.pop()
                    break
                elif game.player.type == HAMMER_TYPE:
                    self.obstacles.remove(obstacle)
                    game.sounds[1].play()
                elif game.player.type == SHIELD_TYPE:
                    return
                elif game.player.type == HEART_TYPE:
                    self.obstacles.pop()
                    game.score -= 100
                    game.player.power_up_time = 0

    def reset_obstacles(self):
        self.obstacles = []

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)