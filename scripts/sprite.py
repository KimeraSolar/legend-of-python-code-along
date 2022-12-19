from numbers import Number
import pygame
from event_timer import Timer
from math import sin
from settings import *

class GenericSprite(pygame.sprite.Sprite):
    def __init__(self, pos : tuple, surface : pygame.Surface, groups: pygame.sprite.Group | list[pygame.sprite.Group] , layer : str = 'main') -> None:
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z_layer = LAYERS[layer]

    def damage(self, attack_type : str, attack_damage : Number) -> None:
        pass
        # print('attacked by', attack_type, 'dealing', attack_damage, 'damage')

class CollidableSprite(GenericSprite):
    def __init__(self, pos : tuple, surface : pygame.Surface, groups: pygame.sprite.Group | list[pygame.sprite.Group], inflation_rate: tuple = (0, -10), layer : str = 'main') -> None:
        super().__init__(pos, surface, groups, layer)
        self.hitbox = self.rect.inflate(inflation_rate)

class DynamicSprite(CollidableSprite):
    def __init__(self, pos : tuple, surface : pygame.Surface, collision_sprites : pygame.sprite.Group, groups: pygame.sprite.Group | list[pygame.sprite.Group], inflation_rate: tuple = (0, -10), layer : str = 'main') -> None:
        super().__init__(pos, surface, groups, layer=layer)
        self.hitbox = self.rect.inflate(inflation_rate)
        self.dynamics_setup(collision_sprites)
        self.timers_setup()
        self.animation_setup()
            
    def timers_setup(self) -> None:
        self.timers = {}
        self.timers['flicker timer'] = Timer(150)
        self.timers['damage cooldown'] = Timer(200)
    
    def update_timers(self) -> None:
        for timer in self.timers.values():
            timer.update()

    def graphics_setup(self) -> None:
        raise NotImplementedError()

    def animation_setup(self) -> None:
        self.frame_index = 0
        self.animation_speed = 0.15

    def dynamics_setup(self, collision_sprites : pygame.sprite.Group) -> None:
        self.collision_sprites = collision_sprites
        self.direction = pygame.math.Vector2()
        self.speed = self.stats['speed']
    
    def move(self, speed : Number) -> None:
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')

        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        self.rect.center = self.hitbox.center

    def collision(self, direction : str) -> None:
        sprites = list(filter(lambda sprite : sprite.hitbox.colliderect(self.hitbox), self.collision_sprites))
        for sprite in sprites:
            if hasattr(sprite, 'hitbox'):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def animate(self) -> None:
        self.frame_index += self.animation_speed
        self.frame_index %= len(self.animations[self.status])
        self.image = self.animations[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if self.timers['flicker timer'].active:
            alpha = self.get_alpha_flicker()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_alpha_flicker(self):
        value = sin(pygame.time.get_ticks())
        value = 255 if value >= 0 else 0
        return value

    def damage(self, attack_type: str, attack_damage: Number) -> None:
        super().damage(attack_type, attack_damage)
        if not self.timers['damage cooldown'].active:
            self.timers['flicker timer'].activate()
            self.health -= attack_damage
            self.timers['damage cooldown'].activate()
        if self.health <= 0:
            self.kill_sprite()

    def kill_sprite(self):
        self.kill()

    def update(self) -> None:
        self.update_timers()
        self.move(self.speed)
        self.animate()