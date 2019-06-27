from game_objects import GameObject
import pygame
import random
from collections import deque


class AssaultSoldier(GameObject):
    def __init__(self,
                 initial_pos=None,
                 initial_vel=(0, 0),
                 move_speed=5,
                 animations=None):
        super().__init__(hitbox=pygame.Rect(initial_pos[0], initial_pos[1], 24, 50),
                         initial_vel=initial_vel,
                         move_speed=move_speed,
                         animations=animations,
                         initial_animation='face_right')

    def update(self, dt, terrain, player_pos):
        self.update_velocity(dt)
        animation = "face_right" if self.move_speed > 0 else "face_left"
        super().update(dt, animation)
        self.update_pos(dt, terrain)

    def update_velocity(self, dt):
        self.y_vel = self.y_vel + dt * GameObject.gravity
        self.y_vel -= self.drag * self.y_vel * dt
        self.x_vel = self.move_speed
        if not self.in_air and random.random() > 0.999:
            self.move_speed *= -1

    def get_sprites(self):
        return [super().get_sprite()]


class WormHead(GameObject):
    def update(self, dt, terrain, player_pos):
        if abs(self.x_vel) > abs(self.y_vel):
            animation = 'head_left' if self.x_vel < 0 else 'head_right'
        else:
            animation = 'head_up' if self.y_vel < 0 else 'head_down'
        super().update(dt, animation)
        self.y += self.y_vel
        self.x += self.x_vel
        self.y_vel += 0.01


class Worm:
    def __init__(self, initial_pos, animations, length=10):
        self.head = WormHead(hitbox=pygame.Rect(initial_pos[0], initial_pos[1], 64, 64),
                             initial_vel=(random.random() * 8 - 4, -random.random() * 5),
                             animations={n: animations[n] for n in animations.keys() if n.startswith("head_")},
                             initial_animation='head_up')
        self.segments = [GameObject(hitbox=pygame.Rect(initial_pos[0], initial_pos[1], 64, 64),
                                    animations={'neutral': animations['segment']}) for _ in range(length)]
        self.image_offset = (0, 0)
        self.hitbox = self.head.hitbox
        self.pos_history = deque([[(self.head.x, self.head.y), *[(s.x, s.y) for s in self.segments]]])

    def update(self, dt, terrain, player_pos):
        self.head.update(dt, terrain, player_pos)
        if len(self.pos_history) > 8:
            update_to = self.pos_history.pop()
            for n, segment in enumerate(self.segments):
                segment.x = update_to[n][0]
                segment.y = update_to[n][1]
        self.pos_history.appendleft([(self.head.x, self.head.y), *[(s.x, s.y) for s in self.segments]])

    def get_sprites(self):
        sprites = [s.get_sprite() for s in reversed(self.segments)]
        sprites.append(self.head.get_sprite())
        return sprites
