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