import pygame
from settings import *
from sprite import CollidableSprite, GenericSprite
from event_timer import Timer

class Tile(CollidableSprite):
    def __init__(self, pos : tuple, groups: pygame.sprite.Group | list[pygame.sprite.Group], sprite_type : str, surface : pygame.Surface = pygame.Surface((TILESIZE, TILESIZE)) , inflation_rate : tuple = (0, -10), layer : str = 'main') -> None:
        surface = surface
        self.sprite_type = sprite_type
        super().__init__(pos, surface, groups, inflation_rate, layer)

    def damage(self, attack_type, attack_damage) -> None:
        _ = attack_damage
        _ = attack_type
        BasicVisualEffect(
            pos= self.rect.topleft,
            surface=self.image,
            groups=self.groups()[0],
            duration=300,
        )
        self.kill()

class BasicVisualEffect(GenericSprite):
    def __init__(self, pos: tuple, surface: pygame.Surface, groups: pygame.sprite.Group | list[pygame.sprite.Group], color=(255, 255, 255), duration = 200, layer : str = 'main') -> None:
        mask_surface = pygame.mask.from_surface(surface)
        new_surface = mask_surface.to_surface(setcolor=color)
        new_surface.set_colorkey((0, 0, 0))
        super().__init__(pos, new_surface, groups, layer)
        self.timer = Timer(duration=duration, on_timeout=self.kill)
        self.timer.activate()
    
    def update(self) -> None:
        self.timer.update()