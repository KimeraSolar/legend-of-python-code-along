import pygame
from sprite import GenericSprite

class YSortedCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100, 200)

    def custom_draw(self, reference : GenericSprite):
        self.offset.x = reference.rect.centerx - self.half_width
        self.offset.y = reference.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite : sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)