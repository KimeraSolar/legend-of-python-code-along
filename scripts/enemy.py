import pygame
from event_timer import Timer
from sprite import DynamicSprite
from player import Player
from utils import import_folder
from settings import *

class Enemy(DynamicSprite):
    def __init__(self, pos: tuple, monster_name : str, collision_sprites: pygame.sprite.Group, groups: pygame.sprite.Group | list[pygame.sprite.Group]) -> None:
        self.sprite_type = 'enemy'
        self.monster_name = monster_name
        self.stats = MONSTER_DATA[monster_name]
        self.animation_setup()
        self.graphics_setup()
        super().__init__(pos, self.animations[self.status][self.frame_index], collision_sprites, groups, inflation_rate=(0, -10))

    def timers_setup(self) -> None:
        super().timers_setup()
        self.timers['attack cooldown'] = Timer(1000)
        self.timers['attack'] = Timer(250)

    def get_player_distance_vector(self, player : Player) -> pygame.math.Vector2:
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = (player_vec - enemy_vec)

        return distance

    def get_status(self, player : Player) -> None:
        distance_vec = self.get_player_distance_vector(player)
        distance = distance_vec.magnitude()
        direction = distance_vec.normalize() if distance > 0 else pygame.math.Vector2()
        self.direction = direction

        if distance <= self.stats['attack_radius'] and not self.timers['attack cooldown'].active:
            self.timers['attack cooldown'].activate()
            self.timers['attack'].activate()
            print('attack')
        elif distance <= self.stats['notice_radius']:
            self.status = 'move'
            self.direction = direction
        else:
            self.status = 'idle'
            self.direction = pygame.math.Vector2()

        if self.timers['attack'].active:
            self.status = 'attack'

    def graphics_setup(self) -> None:
        full_path = GRAPHICS_PATH + 'monsters' + FOLDER_SEPARATOR + self.monster_name + FOLDER_SEPARATOR
        self.animations = { 'idle' : [], 'move': [], 'attack': [] }

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(full_path + animation)

        self.status = 'idle'
    
    def enemy_update(self, player : Player) -> None:
        self.get_status(player)