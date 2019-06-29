from game_objects import Sprite, gravity
import pygame
import random
from collections import deque


class AssaultSoldier:
    def __init__(self,
                 initial_pos=None,
                 move_speed=15,
                 animations=None):
        self.sprite = Sprite(animations=animations,
                             initial_pos=initial_pos,
                             initial_animation='face_right')
        self.move_speed = move_speed
        self.x_vel = move_speed
        self.y_vel = 0
        self.drag = 0.03
        self.in_air = False

    def update(self, dt, terrain, player_pos):
        self.update_velocity(dt)
        animation = "face_right" if self.x_vel > 0 else "face_left"
        self.sprite.update(dt, animation)
        self.update_pos(dt, terrain)

    def update_velocity(self, dt):
        self.y_vel = self.y_vel + dt * gravity
        self.y_vel -= self.drag * self.y_vel * dt
        if not self.in_air and random.random() > 0.999:
            self.x_vel *= -1

    def update_pos(self, dt, terrain):
        hitbox = self.sprite.hitbox
        new_x = self.sprite.x + dt * self.x_vel
        new_y = self.sprite.y + dt * self.y_vel
        moved_x_hb = hitbox.copy()
        moved_x_hb.x = new_x

        moved_y_hb = hitbox.copy()
        moved_y_hb.y = new_y

        x_ok, y_ok = True, True

        for hb in [terrain_object.hitbox for terrain_object in terrain]:
            if hb.top < hitbox.bottom and hb.bottom > hitbox.top:
                if self.x_vel > 0 and moved_x_hb.left < hb.left <= moved_x_hb.right:
                    hitbox.right = hb.left
                    self.x_vel = 0
                    x_ok = False
                elif self.x_vel < 0 and moved_x_hb.right > hb.right >= moved_x_hb.left:
                    hitbox.left = hb.right
                    self.x_vel = 0
                    x_ok = False

            if hb.left < hitbox.right and hb.right > hitbox.left:
                if self.y_vel > 0 and moved_y_hb.top < hb.top <= moved_y_hb.bottom:
                    hitbox.bottom = hb.top
                    self.y_vel = 0
                    self.in_air = False
                    y_ok = False
                elif self.y_vel < 0 and moved_y_hb.bottom > hb.bottom > moved_y_hb.top:
                    hitbox.top = hb.bottom
                    self.y_vel = 0
                    y_ok = False
        if x_ok:
            self.sprite.x = new_x
        if y_ok:
            self.sprite.y = new_y

    def draw(self, surface, coordinate_map):
        image, pos = self.sprite.get_sprite()
        surface.blit(image, coordinate_map(pos))

    @property
    def hitbox(self):
        return self.sprite.hitbox

# class WormHead(GameObject):
#     def update(self, dt, terrain, player_pos):
#         if abs(self.x_vel) > abs(self.y_vel):
#             animation = 'head_left' if self.x_vel < 0 else 'head_right'
#         else:
#             animation = 'head_up' if self.y_vel < 0 else 'head_down'
#         super().update(dt, animation)
#         self.y += self.y_vel
#         self.x += self.x_vel
#         self.y_vel += 0.01
#
#
# class Worm:
#     def __init__(self, initial_pos, animations, length=10):
#         self.head = WormHead(hitbox=pygame.Rect(initial_pos[0], initial_pos[1], 64, 64),
#                              initial_vel=(random.random() * 8 - 4, -random.random() * 5),
#                              animations={n: animations[n] for n in animations.keys() if n.startswith("head_")},
#                              initial_animation='head_up')
#         self.segments = [GameObject(hitbox=pygame.Rect(initial_pos[0], initial_pos[1], 64, 64),
#                                     animations={'neutral': animations['segment']}) for _ in range(length)]
#         self.image_offset = (0, 0)
#         self.hitbox = self.head.hitbox
#         self.pos_history = deque([[(self.head.x, self.head.y), *[(s.x, s.y) for s in self.segments]]])
#
#     def update(self, dt, terrain, player_pos):
#         self.head.update(dt, terrain, player_pos)
#         if len(self.pos_history) > 8:
#             update_to = self.pos_history.pop()
#             for n, segment in enumerate(self.segments):
#                 segment.x = update_to[n][0]
#                 segment.y = update_to[n][1]
#         self.pos_history.appendleft([(self.head.x, self.head.y), *[(s.x, s.y) for s in self.segments]])
#
#     def get_sprites(self):
#         sprites = [s.get_sprite() for s in reversed(self.segments)]
#         sprites.append(self.head.get_sprite())
#         return sprites
