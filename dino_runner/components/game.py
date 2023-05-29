
import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.text import FontEnum, draw_text
sound_files = ['jump_sound.mp3', 'cutting_wood_sound.mp3', 'life_sound.mp3', "damage_sound.mp3"]


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.score = 0
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.sounds = []
        self.load_sounds()
        self.best_score = 0

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.power_up_manager.reset_power_ups()
        self.score = 0
        self.game_speed = 20
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def load_sounds(self):
        for file in sound_files:
            sound = pygame.mixer.Sound(file)
            sound.set_volume(0.2)
            self.sounds.append(sound)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input, self)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self)

    def best_score(self):
        return self.best_score
    
    def update_score(self):
        self.score += 1
        if self.score > self.best_score:
            self.best_score = self.score
        if self.score % 100 == 0:
            self.game_speed += 3
    
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)

            if time_to_show >= 0:
                draw_text(
                    self,
                    f"{self.player.type.capitalize()} enabled for {time_to_show} seconds",
                    500,
                    40
                )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 117, 24))#FFFFFF
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        draw_text(self, f"Score: {self.score}", 1000, 50)
        draw_text(self, f"Deaths: {self.death_count}", 850, 50)
        draw_text(self, f"Best Score: {self.best_score}", 700, 50)
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

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            draw_text(self, "Press any key to start", half_screen_width, half_screen_height, FontEnum.JURASSIC_FONT)
        else:
            self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))
            draw_text(self, "GAME OVER", half_screen_width, half_screen_height, FontEnum.JURASSIC_FONT)
            draw_text(self, f"Score: {self.score}", 1000, 50)
            draw_text(self, f"Deaths: {self.death_count}", 850, 50)
            draw_text(self, f"Best Score: {self.best_score}", 700, 50)

        pygame.display.flip()  

        self.handle_events_on_menu()
