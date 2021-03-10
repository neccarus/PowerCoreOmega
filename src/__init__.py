import pygame
from .game import Game
from .utils import Settings
from .controls import Controls
from .player import Player
from .guis import guis

# initialize pygame.font to avoid import errors
pygame.font.init()

# initialize game_obj to avoid import errors
game_obj = Game("game")

player_controls = Controls(forward=pygame.K_w, backward=pygame.K_s, left=pygame.K_a,
                           right=pygame.K_d, fire_weapon=pygame.K_SPACE)

player_settings = Settings(controls=player_controls, screensize=(1600, 900))

player = Player(controls=player_settings.controls)

main_surface = pygame.Surface(size=player_settings.screensize)
game_surface = pygame.Surface(size=player_settings.screensize)
pause_surface = pygame.Surface(size=player_settings.screensize)

game_obj.bodies = pygame.sprite.Group(player.ship)
game_obj.new_game_state("paused", [guis["pause_gui"]], pause_surface)
game_obj.new_game_state("running", [guis["start_gui"]], main_surface)
game_obj.new_game_state("playing", None, game_surface)
# game_obj.controllers.append(player)
