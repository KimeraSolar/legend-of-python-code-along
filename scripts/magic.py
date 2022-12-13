import pygame
from player import Player
from sprite import GenericSprite
from debug import debug
from settings import *

class Magic(GenericSprite):
    def __init__(self, player : Player, groups: pygame.sprite.Group | list[pygame.sprite.Group]) -> None:
        super().__init__(pos = player.rect.center, surface=pygame.Surface((30, 30)), groups=groups)
        spell = player.get_spell()
        print(spell, MAGIC_DATA[spell]['strength'], MAGIC_DATA[spell]['cost'])
