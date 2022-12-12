import pygame
from settings import *
from sprite import CollidableSprite

class Tile(CollidableSprite):
    def __init__(self, pos : tuple, groups: pygame.sprite.Group | list[pygame.sprite.Group], sprite_type : str, surface : pygame.Surface = pygame.Surface((TILESIZE, TILESIZE)) ) -> None:
        surface = surface
        self.sprite_type = sprite_type
        super().__init__(pos, surface, groups)