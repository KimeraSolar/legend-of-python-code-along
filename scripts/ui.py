import pygame
from settings import *
from player import Player
from debug import debug
from numbers import Number

class UI:
    def __init__(self) -> None:
        self.display_setup()
        self.bar_setup()

    def display_setup(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_SETTINGS['font'], UI_SETTINGS['font size'])

        self.weapon_graphics = {}
        for weapon in WEAPON_DATA.keys():
            weapon_graphic =  pygame.image.load(WEAPON_DATA[weapon]['graphic']).convert_alpha()
            self.weapon_graphics[weapon] = weapon_graphic
        
        self.magic_graphics = {}
        for magic in MAGIC_DATA.keys():
            magic_graphic =  pygame.image.load(MAGIC_DATA[magic]['graphic']).convert_alpha()
            self.magic_graphics[magic] = magic_graphic

    def bar_setup(self) -> None:
        self.health_bar_rect = pygame.Rect(10, 10, UI_SETTINGS['health bar width'], UI_SETTINGS['bar height'])
        self.energy_bar_rect = pygame.Rect(10, 34, UI_SETTINGS['energy bar width'], UI_SETTINGS['bar height'])

    def show_bar(self, current_amount : Number, max_amount : Number, bg_rect : pygame.Rect, color : str) -> None:
        pygame.draw.rect(self.display_surface, UI_SETTINGS['colors']['BG'], bg_rect)

        amount_percentage = current_amount / max_amount
        current_width = bg_rect.width * amount_percentage
        info_rect = bg_rect.copy()
        info_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, info_rect)
        pygame.draw.rect(self.display_surface, UI_SETTINGS['colors']['border'], bg_rect, 3)

    def show_exp(self, exp : Number | str):
        text_surface = self.font.render(str(int(exp)), False, UI_SETTINGS['colors']['text'])
        x = self.display_surface.get_width() - 20
        y = self.display_surface.get_height() - 20
        text_rect = text_surface.get_rect(bottomright=(x,y))

        pygame.draw.rect(self.display_surface, UI_SETTINGS['colors']['BG'], text_rect.inflate(20, 20))
        pygame.draw.rect(self.display_surface, UI_SETTINGS['colors']['border'], text_rect.inflate(20, 20), 3)
        
        self.display_surface.blit(text_surface, text_rect)

    def selection_box(self, left : Number, top : Number, switched : bool) -> pygame.Rect:
        bg_rect = pygame.Rect(left, top, UI_SETTINGS['item box size'], UI_SETTINGS['item box size'])
        pygame.draw.rect(self.display_surface, UI_SETTINGS['colors']['BG'], bg_rect)
        if switched:
            pygame.draw.rect(self.display_surface, UI_SETTINGS['colors']['border active'], bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_SETTINGS['colors']['border'], bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon : str, switched : bool) -> None:
        bg_rect = self.selection_box(10, self.display_surface.get_height() - 100, switched)
        weapon_surface = self.weapon_graphics[weapon]
        weapon_rect = weapon_surface.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surface, weapon_rect)

    def magic_overlay(self, magic : str, switched : bool) -> None:
        bg_rect = self.selection_box(80, self.display_surface.get_height() - 95, switched)
        magic_surface = self.magic_graphics[magic]
        magic_rect = magic_surface.get_rect(center= bg_rect.center)
        self.display_surface.blit(magic_surface, magic_rect)

    def display(self, player : Player) -> None:
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, UI_SETTINGS['colors']['health']) 
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, UI_SETTINGS['colors']['energy'])

        self.show_exp(player.exp)
        
        self.magic_overlay(player.get_spell(), player.timers['magic switch cooldown'].active)
        self.weapon_overlay(player.get_weapon(), player.timers['weapon switch cooldown'].active)
        