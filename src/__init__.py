import pygame
from .game import Game
from .utils import Settings
from .controls import Controls
from .player import Player

# initialize pygame.font to avoid import errors
pygame.font.init()

# initialize game_obj to avoid import errors
game_obj = Game("game")

player_controls = Controls(forward=pygame.K_w, backward=pygame.K_s, left=pygame.K_a,
                           right=pygame.K_d, fire_weapon=pygame.K_SPACE)

player_settings = Settings(controls=player_controls, screensize=(1600, 900))

player = Player(controls=player_settings.controls)

game_obj.bodies = pygame.sprite.Group(player.ship)
game_obj.controllers.append(player)
