import pygame
from sprite import GenericSprite
from player import Player
from settings import *
from numbers import Number

class Attack(GenericSprite):
    def __init__(self, pos: tuple, attack_damage : Number, attack_type : str, surface : pygame.Surface, groups: pygame.sprite.Group | list[pygame.sprite.Group], layer= 'weapon') -> None:
        super().__init__(pos = pos, surface=surface, groups=groups, layer=layer)
        self.attack_damage = attack_damage 
        self.attack_type = attack_type

    def get_damage(self) -> Number:
        return self.attack_damage

    def get_type(self) -> str:
        return self.attack_type

class Weapon(Attack):
    def __init__(self, player : Player, groups: pygame.sprite.Group | list[pygame.sprite.Group], layer= 'weapon') -> None:
        attack_type = player.get_weapon()
        attack_damage = player.stats['attack'] + WEAPON_DATA[attack_type]['damage']
        
        direction = player.status.split('_')[0]
        full_path = GRAPHICS_PATH + 'weapons' + FOLDER_SEPARATOR + player.get_weapon() + FOLDER_SEPARATOR + direction + '.png'
        surface = pygame.image.load(full_path).convert_alpha()
        super().__init__(
            pos = player.rect.center, 
            surface=surface, 
            groups=groups, 
            layer=layer,
            attack_type=attack_type,
            attack_damage=attack_damage,
        )
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10, 0))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10, 0))    
        print(self.attack_type, self.attack_damage)

class Magic(Attack):
    def __init__(self, player : Player, groups: pygame.sprite.Group | list[pygame.sprite.Group], layer= 'magic') -> None:
        attack_type = player.get_spell()
        attack_damage = player.stats['attack'] + MAGIC_DATA[attack_type]['strength']
        self.attack_cost = MAGIC_DATA[attack_type]['cost']
        super().__init__(
            pos = player.rect.center, 
            surface=pygame.Surface((30, 30)), 
            groups=groups,
            attack_type=attack_type,
            attack_damage=attack_damage,
            layer=layer,
        )
        print(self.attack_type, self.attack_damage, self.attack_cost)
