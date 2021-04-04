import pygame
from .game import Game
from .utils import Settings, setting_defaults
from .controls import Controls
from .player import Player
import os

cwd = os.getcwd()

# Initialize Pygame
pygame.init()

# Check if system is Linux based to avoid sound problems
if os.name == 'posix':
    os.environ['SDL_AUDIODRIVER'] = 'dsp'

os.environ['SDL_VIDEO_CENTERED'] = '1'

# initialize game_obj to avoid import errors
game_obj = Game("game")

try:
    player_settings = Settings.load_settings(os.path.join(cwd, 'settings.json'))
except (OSError, IOError) as e:
    print(e)
    Settings.save_new_settings('settings.json', setting_defaults)
    player_settings = Settings.load_settings(os.path.join(cwd, 'settings.json'))

screen = pygame.display.set_mode(player_settings.screensize,
                                 pygame.FULLSCREEN * player_settings.fullscreen | pygame.SCALED | pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Power Core Omega")
