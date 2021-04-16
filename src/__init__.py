import pygame
from .utils import Settings, setting_defaults, load_single_sprite
from .controls import Controls
import os

cwd = os.getcwd()

# Initialize Pygame
pygame.init()

# Check if system is Linux based to avoid sound problems
if os.name == 'posix':
    os.environ['SDL_AUDIODRIVER'] = 'dsp'

os.environ['SDL_VIDEO_CENTERED'] = '1'

# ship sprites loaded here to avoid cwd issues on Mac
ship_sprite_dict = {"Python": load_single_sprite(os.path.join(cwd, 'graphics', 'ships'), 'Python_Ship_rev2.png'),
                    "Cestus": load_single_sprite(os.path.join(cwd, 'graphics', 'ships'), 'Cestus_Ship_rev1.png'),
                    "Broadsword": load_single_sprite(os.path.join(cwd, 'graphics', 'ships'), 'Broadsword_Ship_rev1.png'),
                    "Mud Skipper": load_single_sprite(os.path.join(cwd, 'graphics', 'ships'), 'Basic_Enemy_Ship_rev1.png')}

from .game import Game

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

