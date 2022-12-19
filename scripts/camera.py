import pygame
from sprite import GenericSprite
from player import Player
from settings import *

class YSortedCameraGroup(pygame.sprite.Group):
    def __init__(self, enemy_sprites : pygame.sprite.Group) -> None:
        super().__init__()
        
        self.enemy_sprites = enemy_sprites
        
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100, 200)

        self.floor_surface = pygame.image.load(GRAPHICS_PATH + 'tilemap' + FOLDER_SEPARATOR + 'ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

    def enemy_update(self, player : Player) -> None:
        for enemy in self.enemy_sprites:
            enemy.enemy_update(player)

    def custom_draw(self, reference : GenericSprite):
        self.offset.x = reference.rect.centerx - self.half_width
        self.offset.y = reference.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        for layer in LAYERS.values():
            sprites = filter(  lambda s : s.z_layer == layer , self.sprites())
            for sprite in sorted(sprites, key=lambda sprite : sprite.rect.centery):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)