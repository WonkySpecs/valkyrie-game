import random
from enum import Enum

import pygame

import enemy_classes
from game_objects import Player
from game_state import GameState
from terrain import Terrain


class LevelOne:
    def __init__(self, asset_factory):
        self.asset_factory = asset_factory

    def update(self, dt, game_state):
        game_state.increment_timers(dt)

    @property
    def initial_game_state(self):
        assets = self.asset_factory
        bg_sprite = assets.get_background()
        terrain = [Terrain(initial_pos=pygame.Vector2(-200, 0), animations=assets.wall_animation(900, 50)),
                   Terrain(initial_pos=pygame.Vector2(-200, 800), animations=assets.wall_animation(900, 15)),
                   Terrain(initial_pos=pygame.Vector2(-200, 0), animations=assets.wall_animation(20, 800)),
                   Terrain(initial_pos=pygame.Vector2(700, 0), animations=assets.wall_animation(50, 800)),
                   Terrain(initial_pos=pygame.Vector2(300, 300), animations=assets.wall_animation(50, 50)),
                   Terrain(initial_pos=pygame.Vector2(200, 500), animations=assets.platform_animation(300, 8), platform=True),
                   Terrain(initial_pos=pygame.Vector2(200, 600), animations=assets.platform_animation(300, 8), platform=True)]

        state = GameState(
            player=Player(animations=assets.player_animations(), initial_pos=pygame.Vector2(320, 50)),
            enemies=[*[enemy_classes.AssaultSoldier(initial_pos=pygame.Vector2(50 + x, 400),
                                                    move_speed=random.randint(3, 6),
                                                    animations=assets.assault_soldier_green())
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
