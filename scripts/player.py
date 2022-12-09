import pygame
from settings import *
from sprite import CollidableSprite
from numbers import Number

class Player(CollidableSprite):
    def __init__(self, pos : tuple, collision_sprites : pygame.sprite.Group, groups:  pygame.sprite.Group | list[pygame.sprite.Group] ) -> None:
        surface = pygame.image.load(GRAPHICS_PATH + 'test' + FOLDER_SEPARATOR + 'player.png').convert_alpha()
        super().__init__(pos, surface, groups, inflation_rate=(0, -26))
        self.dynamics_setup(collision_sprites)
    
    def dynamics_setup(self, collision_sprites : pygame.sprite.Group) -> None:
        self.collision_sprites = collision_sprites
        self.direction = pygame.math.Vector2()
        self.speed = 5

    def input(self) -> None:
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_UP]:
            self.direction.y = -1
        elif pressed_keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if pressed_keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif pressed_keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
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

    def update(self) -> None:
        self.input()
        self.move(self.speed)