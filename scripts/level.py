import pygame
from settings import *
from tile import Tile
from utils import import_csv_layout, import_folder
from player import Player
from camera import YSortedCameraGroup
from debug import debug
from random import choice

class Level:
    def __init__(self) -> None:
        self.sprites_groups_setup()
        self.map_setup()

    def sprites_groups_setup(self) -> None:
        self.visible_sprites = YSortedCameraGroup()
        self.collision_sprites = pygame.sprite.Group()

    def map_setup(self) -> None:
        layouts = {
            'boundary' : import_csv_layout(MAP_PATH + 'map_FloorBlocks.csv'),
            'grass' : import_csv_layout(MAP_PATH + 'map_Grass.csv'),
            'large object' : import_csv_layout(MAP_PATH + 'map_LargeObjects.csv'),
        }

        graphics = {
            'grass' : import_folder(GRAPHICS_PATH + 'grass'),
            'objects': import_folder(GRAPHICS_PATH + 'objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, cel in enumerate(row):
                    if cel != '-1':
                        x = col_index*TILESIZE
                        y = row_index*TILESIZE
                        if style == 'boundary':
                            Tile(
                                pos=(x,y),
                                groups=[self.collision_sprites],
                                sprite_type='invisible',
                            )
                        elif style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                pos=(x, y),
                                groups=[self.visible_sprites, self.collision_sprites],
                                sprite_type='grass',
                                surface=random_grass_image
                            )
                        elif style == 'large object':
                            surface = graphics['objects'][int(cel)]
                            y = y - TILESIZE # large objects have twice the size of other objects
                            Tile(
                                pos=(x, y),
                                groups=[self.visible_sprites, self.collision_sprites],
                                sprite_type='large object',
                                surface=surface
                            )

        self.player = Player(
            pos=(2000,1430),
            collision_sprites=self.collision_sprites,
            groups=self.visible_sprites
        )

    def run(self) -> None:
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug('debug mode on')