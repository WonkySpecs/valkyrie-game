from enum import Enum
import math
import random

import pygame

from game_objects import Player, Projectile
from terrain import Terrain
import enemy_classes
from game_state import GameState


class LevelOne:
    def __init__(self, asset_factory):
        self.timer = 0
        self.assets = asset_factory

    def update(self, dt, game_state):
        pass

    @property
    def initial_game_state(self):
        bg_sprite = self.assets.get_background()
        terrain = [Terrain(initial_pos=pygame.Vector2(-200, 0), animations=self.assets.wall_animation(900, 50)),
                   Terrain(initial_pos=pygame.Vector2(-200, 800), animations=self.assets.wall_animation(900, 15)),
                   Terrain(initial_pos=pygame.Vector2(-200, 0), animations=self.assets.wall_animation(20, 800)),
                   Terrain(initial_pos=pygame.Vector2(700, 0), animations=self.assets.wall_animation(50, 800)),
                   Terrain(initial_pos=pygame.Vector2(300, 300), animations=self.assets.wall_animation(50, 50)),
                   Terrain(initial_pos=pygame.Vector2(200, 500), animations=self.assets.platform_animation(300, 8), platform=True),
                   Terrain(initial_pos=pygame.Vector2(200, 600), animations=self.assets.platform_animation(300, 8), platform=True)]

        state = GameState(
            player=Player(animations=self.assets.player_animations(), initial_pos=pygame.Vector2(320, 50)),
            enemies=[*[enemy_classes.AssaultSoldier(initial_pos=pygame.Vector2(50 + x, 400),
                                                    move_speed=random.randint(3, 6),
                                                    animations=self.assets.assault_soldier_green())
                       for x in range(50, 600, 25)]],
            terrain=terrain,
            background_layers={0: [(bg_sprite, pygame.Vector2(-350, -300))]},
            clock=pygame.time.Clock(),
            hud={'font': pygame.font.Font(None, 20)}
        )
        return state


class Level(Enum):
    ONE = LevelOne

    @staticmethod
    def load(level, asset_factory):
        return level.value(asset_factory)
