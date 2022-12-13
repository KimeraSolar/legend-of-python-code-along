import pygame
from typing import Callable
from numbers import Number

class Timer:
    def __init__(self, duration : Number, on_count : Callable = None, on_timeout : Callable = None) -> None:
        self.duration = duration
        self.on_count = on_count
        self.on_timeout = on_timeout
        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.on_timeout and self.start_time != 0:
                self.on_timeout()
            self.deactivate()
        elif self.on_count:
            self.on_count()