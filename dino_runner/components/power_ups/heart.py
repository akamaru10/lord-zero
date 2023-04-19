from dino_runner.utils.constants import HEART, DEFAULT_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class Heart(PowerUp):
    def __init__(self):
        super().__init__(HEART, DEFAULT_TYPE)