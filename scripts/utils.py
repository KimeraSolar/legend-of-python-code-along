import pygame
from csv import reader
from os import walk
from settings import *

def import_csv_layout(path):
    layout_resp = []
    with open(path) as file:
        layout = reader(file, delimiter=',')
        for row in layout:
            layout_resp.append(list(row))

    return layout_resp


def import_folder(path):
    resp = []
    for _, _, data in walk(path):
        for file in data:
            full_path = path + FOLDER_SEPARATOR + file
            surface = pygame.image.load(full_path).convert_alpha()
            resp.append(surface)
    return resp