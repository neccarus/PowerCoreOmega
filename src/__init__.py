import pygame
from .game import Game

# initialize pygame.font to avoid import errors
pygame.font.init()
SCREENSIZE = (1600, 900)

# initialize game_obj to avoid import errors
game_obj = Game()
