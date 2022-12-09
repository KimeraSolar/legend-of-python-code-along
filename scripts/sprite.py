import pygame
from settings import *


class GenericSprite(pygame.sprite.Sprite):
    def __init__(self, pos : tuple, surface : pygame.Surface, groups: pygame.sprite.Group | list[pygame.sprite.Group] ) -> None:
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)


class CollidableSprite(GenericSprite):
    def __init__(self, pos : tuple, surface : pygame.Surface, groups: pygame.sprite.Group | list[pygame.sprite.Group], inflation_rate: tuple = (0, -10)) -> None:
        super().__init__(pos, surface, groups)
        self.hitbox = self.rect.inflate(inflation_rate)