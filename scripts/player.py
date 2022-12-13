import pygame
from typing import Callable
from event_timer import Timer
from settings import *
from sprite import DynamicSprite
from numbers import Number
from utils import import_folder

class Player(DynamicSprite):
    def __init__(self, pos : tuple, collision_sprites : pygame.sprite.Group, groups:  pygame.sprite.Group | list[pygame.sprite.Group], create_attack : Callable, destroy_attack : Callable, create_magic : Callable, destroy_magic : Callable) -> None:
        surface = pygame.image.load(GRAPHICS_PATH + 'test' + FOLDER_SEPARATOR + 'player.png').convert_alpha()
        self.stats_setup()
        self.attack_setup(create_attack, destroy_attack, create_magic, destroy_magic)
        self.graphics_setup()
        super().__init__(pos, surface, collision_sprites, groups, inflation_rate=(-10, -20))

    def graphics_setup(self) -> None:
        character_path = GRAPHICS_PATH + 'player' + FOLDER_SEPARATOR
        self.animations = {
            'up' : [], 'down' : [], 'left' : [], 'right' : [],
            'up_idle' : [], 'down_idle' : [], 'left_idle' : [], 'right_idle' : [],
            'up_attack' : [], 'down_attack' : [], 'left_attack' : [], 'right_attack' : [],
        }

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(character_path + animation)

        self.status = 'down'

    def stats_setup(self) -> None:
        self.stats = {'health' : 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123

    def attack_setup(self, create_attack : Callable, destroy_attack: Callable, create_magic : Callable, destroy_magic: Callable)  -> None:
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.create_magic = create_magic
        self.destroy_magic = destroy_magic
        self.weapon_index = 0
        self.weapons = list(WEAPON_DATA.keys())
        self.magic_index = 0
        self.magics = list(MAGIC_DATA.keys())
    
    def timers_setup(self) -> None:
        super().timers_setup()
        self.timers['attack'] = Timer(200, on_timeout=self.destroy_attack)
        self.timers['weapon switch cooldown'] = Timer(300)
        self.timers['magic'] = Timer(200, on_timeout=self.destroy_magic)
        self.timers['magic switch cooldown'] = Timer(300)
        self.timers['action cooldown'] = Timer(500)

    def input(self) -> None:
        pressed_keys = pygame.key.get_pressed()

        # movement inputs
        if pressed_keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif pressed_keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if pressed_keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif pressed_keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        # attack inputs
        if pressed_keys[pygame.K_SPACE] and not self.timers['action cooldown'].active:
            self.create_attack()
            self.timers['action cooldown'].activate()
            self.timers['attack'].activate()

        if pressed_keys[pygame.K_RETURN] and not self.timers['action cooldown'].active:
            self.create_magic()
            self.timers['action cooldown'].activate()
            self.timers['magic'].activate()

        # magic inputs
        if pressed_keys[pygame.K_LALT] and not self.timers['weapon switch cooldown'].active:
            self.timers['weapon switch cooldown'].activate()
            self.weapon_index += 1
            self.weapon_index %= len(self.weapons)

        if pressed_keys[pygame.K_LCTRL] and not self.timers['magic switch cooldown'].active:
            self.timers['magic switch cooldown'].activate()
            self.magic_index += 1
            self.magic_index %= len(self.magics)

    def get_status(self) -> None:
        if self.timers['attack'].active:
            self.status = self.status.split('_')[0] + '_attack'
        elif self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'

    def get_weapon(self) -> str:
        return self.weapons[self.weapon_index]

    def get_spell(self) -> str:
        return self.magics[self.magic_index]

    def move(self, speed: Number) -> None:
        if self.timers['attack'].active or self.timers['magic'].active:
            return
        super().move(speed)

    def update(self) -> None:
        self.input()
        self.get_status()
        super().update()