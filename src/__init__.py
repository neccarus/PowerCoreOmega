import pygame
from .game import Game
from .utils import Settings, setting_defaults
from .controls import Controls
from .player import Player


# initialize pygame.font to avoid import errors
pygame.font.init()

# initialize game_obj to avoid import errors
game_obj = Game("game")

player_controls = Controls(forward=[pygame.K_w, pygame.K_UP], backward=[pygame.K_s, pygame.K_DOWN], left=[pygame.K_a, pygame.K_LEFT],
                           right=[pygame.K_d, pygame.K_RIGHT], fire_weapon=[pygame.K_SPACE, ])

try:
    player_settings = Settings.load_settings('settings.json')
except Exception:
    Settings.save_new_settings('settings.json', setting_defaults)
    player_settings = Settings.load_settings('settings.json')
