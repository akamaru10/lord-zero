import random

from dino_runner.components.clouds.cloud_manager import Cloud
from dino_runner.utils.constants import CLOUD



class Cloud(CLOUD):
    def __init__(self, images):
        super().__init__(images)

        self.rect.y =80