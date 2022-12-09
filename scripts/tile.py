import pygame
from settings import *
from sprite import CollidableSprite

class Tile(CollidableSprite):
    def __init__(self, pos : tuple, groups: pygame.sprite.Group | list[pygame.sprite.Group] ) -> None:
        surface =  pygame.image.load(GRAPHICS_PATH + 'test' + FOLDER_SEPARATOR + 'rock.png').convert_alpha()
        super().__init__(pos, surface, groups)