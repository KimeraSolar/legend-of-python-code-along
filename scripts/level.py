import pygame
from settings import *
from tile import Tile
from player import Player
from camera import YSortedCameraGroup
from debug import debug

class Level:
    def __init__(self) -> None:


        self.sprites_groups_setup()
        self.map_setup()

    def sprites_groups_setup(self) -> None:
        self.visible_sprites = YSortedCameraGroup()
        self.collision_sprites = pygame.sprite.Group()

    def map_setup(self) -> None:
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, cel in enumerate(row):
                x = col_index*TILESIZE
                y = row_index*TILESIZE
                if cel == 'x':
                    Tile(
                        pos=(x,y),
                        groups=[self.visible_sprites, self.collision_sprites]
                    )
                elif cel == 'p':
                    self.player = Player(
                        pos=(x,y),
                        collision_sprites=self.collision_sprites,
                        groups=self.visible_sprites
                    )

    def run(self) -> None:
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug('debug mode on')