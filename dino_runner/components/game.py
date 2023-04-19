import pygame
import time

from dino_runner.utils.constants import *
from dino_runner.utils.constants import BG,ICON,SCREEN_HEIGHT,SCREEN_WIDTH,TITLE,FPS
from dino_runner.utils.text_utils import *
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.score = 0
        self.font = pygame.font.Font(FONT_STYLE)
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        MENU.stop ()
        GAME.set_volume (0.3)
        GAME.play(-1)

        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.reset()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def reset(self):
        self.lifes_left = 3
        self.game_speed = 20
        self.score = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5

    def draw_text(self, phrase, size, position, rgb):
        font = pygame.font.Font(FONT_STYLE, size)
        text = font.render(phrase, True, rgb)
        text_rect = text.get_rect()
        text_rect.center = position
        self.screen.blit(text, text_rect)

    def draw_score(self):
        self.draw_text(
            f"Score: {self.score}", 22,
            (1000, 50), (0,0,0))
    
    def hearts_left(self):
        self.draw_text(
                f"Hearts Left: {self.lifes_left}", 22, 
                (1000, 80), (195,0,0))
        
    def draw_power_up_time(self):
        if self.player.has_power_ups:
            if self.player.extra_life:
                self.player.has_power_ups = False
                self.player.type = DEFAULT_TYPE
                self.player.extra_life = False
            else:
                time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)

                if time_to_show >= 0:
                    self.draw_text(
                        f"{self.player.type.capitalize()} for {time_to_show} seconds", 22,
                        (500, 40), (0,0,0))
                    
                else:
                    self.player.has_power_ups = False
                    self.player.type = DEFAULT_TYPE

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.hearts_left()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_parallax(self):
        pass

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        MENU.set_volume (0.3)
        MENU.play (-1)
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        
        if self.death_count == 0:
            font = pygame.font.Font(FONT_STYLE, 22)
            text = font.render("Press any key to start", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(text, text_rect)
        else:
            self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))

            self.draw_text(
                "Press any key to Restart", 22,
                (half_screen_width, half_screen_height), (0,0,0))
            
            self.draw_text(
                f"Deaths: {self.death_count}", 22, 
                (half_screen_width, 80), (195,0,0) )
            
            self.draw_text(
                f"Score: {self.score}", 22,
                (half_screen_width, half_screen_height + 40), (0,0,0) )

    
        pygame.display.flip()

        self.handle_events_on_menu()