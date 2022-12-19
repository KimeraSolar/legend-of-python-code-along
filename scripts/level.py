import pygame
from attack import Weapon, Magic
from settings import *
from tile import Tile
from utils import import_csv_layout, import_folder
from player import Player
from enemy import Enemy
from camera import YSortedCameraGroup
from ui import UI
from numbers import Number
from random import choice

class Level:
    def __init__(self) -> None:
        self.sprites_groups_setup()
        self.map_setup()
        self.attack_setup()
        self.ui_setup()
        self.running = True

    def ui_setup(self) -> None:
        self.ui = UI()

    def sprites_groups_setup(self) -> None:
        self.collision_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.visible_sprites = YSortedCameraGroup(self.enemies)

    def map_setup(self) -> None:
        layouts = {
            'boundary' : import_csv_layout(MAP_PATH + 'map_FloorBlocks.csv'),
            'grass' : import_csv_layout(MAP_PATH + 'map_Grass.csv'),
            'large object' : import_csv_layout(MAP_PATH + 'map_LargeObjects.csv'),
            'entities' : import_csv_layout(MAP_PATH + 'map_Entities.csv')
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
                                groups=[self.visible_sprites, self.collision_sprites, self.attackable_sprites],
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
                                surface=surface,
                                inflation_rate=(-30, -90),
                            )
                        elif style == 'entities':
                            if cel == '394':
                                self.player = Player(
                                    pos=(x, y),
                                    collision_sprites=self.collision_sprites,
                                    groups=self.visible_sprites,
                                    create_attack = self.create_attack,
                                    destroy_attack = self.destroy_attack,
                                    create_magic = self.create_magic,
                                    destroy_magic = self.destroy_magic,
                                    end_game = self.game_over,
                                )
                            else:
                                if cel == '390' : monster_name = 'bamboo'
                                elif cel == '391' : monster_name = 'spirit'
                                elif cel == '392' : monster_name = 'raccoon'
                                else : monster_name = 'squid'
                                Enemy(
                                    pos=(x, y),
                                    collision_sprites=self.collision_sprites,
                                    groups=[self.visible_sprites, self.enemies, self.attackable_sprites],
                                    monster_name=monster_name,
                                    hit_player=self.enemy_attack,
                                )

    def attack_setup(self) -> None:
        self.current_attack = None
        self.current_spell = None

    def create_attack(self) -> None:
        self.current_attack = Weapon(self.player, groups=[self.visible_sprites, self.attack_sprites])

    def destroy_attack(self) -> None:
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_magic(self) -> None:
        self.current_spell = Magic(self.player, groups=[self.visible_sprites, self.attack_sprites])

    def destroy_magic(self) -> None:
        if self.current_spell:
            self.current_spell.kill()
        self.current_spell = None

    def player_attack(self) -> None:
        for attack_sprite in self.attack_sprites:
            attacked_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
            for attacked_sprite in attacked_sprites:
                attacked_sprite.damage(
                    attack_type=attack_sprite.get_type(),
                    attack_damage=attack_sprite.get_damage()
                )

    def enemy_attack(self, attack_type : str, attack_damage : Number):
        self.player.damage(attack_type, attack_damage)

    def game_over(self):
        print('game over D:')
        self.running = False

    def run(self) -> None:
        if self.running:
            self.visible_sprites.custom_draw(self.player)
            self.visible_sprites.enemy_update(self.player)
            self.player_attack()
            self.visible_sprites.update()
            self.ui.display(self.player)