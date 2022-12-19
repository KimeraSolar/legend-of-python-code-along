# game setup
import sys

IS_WINDOWS = sys.platform.startswith('win')

WIDTH    = 1280	// 1.4
HEIGTH   = 720 // 1.4
FPS      = 60
TILESIZE = 64

FOLDER_SEPARATOR = '\\' if IS_WINDOWS else '/'

GRAPHICS_PATH = '.' + FOLDER_SEPARATOR + 'assets' + FOLDER_SEPARATOR + 'graphics' + FOLDER_SEPARATOR

AUDIO_PATH = '.' + FOLDER_SEPARATOR + 'assets' + FOLDER_SEPARATOR + 'audio' + FOLDER_SEPARATOR

MAP_PATH =  '.' + FOLDER_SEPARATOR + 'assets' + FOLDER_SEPARATOR + 'map' + FOLDER_SEPARATOR

WEAPON_DATA = {
    'sword' : { 'cooldown' : 100, 'damage' : 15, 'graphic' : GRAPHICS_PATH + 'weapons' + FOLDER_SEPARATOR + 'sword' + FOLDER_SEPARATOR + 'full.png'},
    'lance' : { 'cooldown' : 400, 'damage' : 30, 'graphic' : GRAPHICS_PATH + 'weapons' + FOLDER_SEPARATOR + 'lance' + FOLDER_SEPARATOR + 'full.png'},
    'axe' : { 'cooldown' : 300, 'damage' : 20, 'graphic' : GRAPHICS_PATH + 'weapons' + FOLDER_SEPARATOR + 'axe' + FOLDER_SEPARATOR + 'full.png'},
    'rapier' : { 'cooldown' : 50, 'damage' : 8, 'graphic' : GRAPHICS_PATH + 'weapons' + FOLDER_SEPARATOR + 'rapier' + FOLDER_SEPARATOR + 'full.png'},
    'sai' : { 'cooldown' : 80, 'damage' : 10, 'graphic' : GRAPHICS_PATH + 'weapons' + FOLDER_SEPARATOR + 'sai' + FOLDER_SEPARATOR + 'full.png'},
}

MAGIC_DATA = {
    'flame' : { 'strength' : 5, 'cost' : 20, 'graphic' : GRAPHICS_PATH + 'particles' + FOLDER_SEPARATOR + 'flame' + FOLDER_SEPARATOR + 'fire.png'},
    'heal' : { 'strength' : 20, 'cost' : 10, 'graphic' : GRAPHICS_PATH + 'particles' + FOLDER_SEPARATOR + 'heal' + FOLDER_SEPARATOR + 'heal.png'},
}

UI_SETTINGS = {
    'bar height' : 20,
    'health bar width' : 200,
    'energy bar width' : 140,
    'item box size' : 80,
    'font' : GRAPHICS_PATH + 'font' + FOLDER_SEPARATOR + 'joystix.ttf',
    'font size' : 18,
    'colors' : {
        'border' : '#111111',
        'text' : '#EEEEEE',
        'BG' : '#222222',
        'health' : 'red',
        'energy' : 'blue',
        'border active' : 'gold',
    },    
}

MONSTER_DATA = {
    'squid' : { 'health': 100, 'exp': 100, 'damage':20, 'attack_type': 'slash', 'attack_sound' : AUDIO_PATH + 'attack' + FOLDER_SEPARATOR + 'slash.wav', 'speed' : 3, 'resistance' : 3, 'attack_radius': 80, 'notice_radius':360},
    'raccoon' : { 'health': 300, 'exp': 250, 'damage':40, 'attack_type': 'claw', 'attack_sound' : AUDIO_PATH + 'attack' + FOLDER_SEPARATOR + 'claw.wav', 'speed' : 2, 'resistance' : 3, 'attack_radius': 120, 'notice_radius':400},
    'spirit' : { 'health': 100, 'exp': 110, 'damage':8, 'attack_type': 'thunder', 'attack_sound' : AUDIO_PATH + 'attack' + FOLDER_SEPARATOR + 'fireball.wav', 'speed' : 4, 'resistance' : 3, 'attack_radius': 60, 'notice_radius':350},
    'bamboo' : { 'health': 70, 'exp': 120, 'damage':6, 'attack_type': 'leaf_attack', 'attack_sound' : AUDIO_PATH + 'attack' + FOLDER_SEPARATOR + 'slash.wav', 'speed' : 3, 'resistance' : 3, 'attack_radius': 50, 'notice_radius':300},
}

LAYERS = {
    'main' : 5,
    'weapon' : 6,
    'magic' : 7,
}