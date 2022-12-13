import pygame
from sprite import GenericSprite
from player import Player
from settings import *

class Weapon(GenericSprite):
    def __init__(self, player : Player, groups: pygame.sprite.Group | list[pygame.sprite.Group]) -> None:
        direction = player.status.split('_')[0]
        full_path = GRAPHICS_PATH + 'weapons' + FOLDER_SEPARATOR + player.get_weapon() + FOLDER_SEPARATOR + direction + '.png'
        surface = pygame.image.load(full_path).convert_alpha()
        super().__init__(pos = player.rect.center, surface=surface, groups=groups)
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10, 0))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10, 0))