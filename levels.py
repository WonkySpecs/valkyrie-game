from enum import Enum
import math
import random

import pygame

from game_objects import Player, Terrain, Projectile
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
                   Terrain(initial_pos=pygame.Vector2(300, 300), animations=self.assets.wall_animation(50, 50))]

        def fire_gun(target_pos, start_pos):
            d_pos = target_pos - start_pos
            theta = math.atan2(d_pos.y, d_pos.x)
            x_vel = 40 * math.cos(theta)
            y_vel = 40 * math.sin(theta)
            return Projectile(initial_vel=pygame.Vector2(x_vel, y_vel),
                              animations=self.assets.yellow_bullet(),
                              initial_pos=start_pos,
                              damage=100)

        state = GameState(
            player=Player(animations=self.assets.player_animations(), initial_pos=pygame.Vector2(320, 50),
                          fire_gun=fire_gun),
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
