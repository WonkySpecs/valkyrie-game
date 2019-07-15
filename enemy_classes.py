from game_objects import VelocityUpdates, BlockedByTerrain, Projectile
import pygame
import random
import math


class AssaultSoldier(BlockedByTerrain):
    def __init__(self,
                 initial_pos=None,
                 move_speed=5,
                 animations=None):
        super().__init__(animations=animations,
                         initial_pos=initial_pos,
                         initial_animation='face_right')
        self.move_speed = move_speed
        self.moving_right = random.random() > 0.5
        self.x_vel = move_speed if self.moving_right else -move_speed
        self.y_vel = 0
        self.drag = 0.03
        self.in_air = False
        self.health = 1000
        self.shooting_at = None
        self.range = 400
        self.shots_in_burst = 3
        self.shots_fired = 0
        self.fire_delay = 25
        self.pre_fire_delay = 180
        self.pre_fire_waited = 0
        self.shot_cooldown = 0
        self.bullet_animation = animations['projectile']

    def update(self, dt, terrain, player_pos):
        if not self.shooting_at and pygame.Vector2(self.hitbox.center).distance_to(player_pos) < self.range:
            self.shooting_at = player_pos
        else:
            self.moving_right = player_pos.x > self.hitbox.center[0]

        self.update_velocity(dt)
        animation = "face_right" if self.moving_right > 0 else "face_left"
        self.sprite.update(dt, animation)
        self.update_pos(dt, terrain)

        if self.shooting_at:
            if self.shots_fired < self.shots_in_burst:
                if self.pre_fire_waited < self.pre_fire_delay:
                    self.pre_fire_waited += 1
                else:
                    if self.shot_cooldown < self.fire_delay:
                        self.shot_cooldown += 1
                    else:
                        return self.shoot()
            else:
                self.shooting_at = None
                self.shots_fired = 0
                self.pre_fire_waited = 0

    def update_velocity(self, dt):
        VelocityUpdates.gravity(self, dt)
        VelocityUpdates.drag(self, dt)
        if not self.in_air:
            if not self.shooting_at:
                self.x_vel = self.move_speed if self.moving_right else -self.move_speed
            else:
                self.x_vel = 0

    def shoot(self):
        self.shots_fired += 1
        self.shot_cooldown = 0
        return Projectile(initial_vel=Projectile.calculate_proj_velocity(self.shooting_at, self.hitbox.center, 5),
                          animations=self.bullet_animation.copy(),
                          initial_pos=pygame.Vector2(self.hitbox.center),
                          damage=10)

    def take_damage(self, proj):
        self.health -= proj.damage
        knockback = proj.damage / 20
        self.y_vel -= knockback
        self.x_vel = knockback if proj.x_vel > 0 else -knockback
        if self.health <= 0:
            self.to_remove = True

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
