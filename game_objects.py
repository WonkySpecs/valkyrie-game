import pygame
import asset_factory


class GameObject:
    gravity = 2.3

    def __init__(self, hitbox=None, initial_vel=(0, 0), move_speed=0,
                 animations=None, initial_animation="neutral", image_offset=(0, 0)):
        self.hitbox = hitbox
        self.x_vel, self.y_vel = initial_vel
        self.move_speed = move_speed
        self.animations = animations
        self.animation_timer = 0
        self.animation = animations[initial_animation]
        self.image_offset = image_offset

    @property
    def x(self):
        return self.hitbox.left

    @x.setter
    def x(self, x):
        self.hitbox.left = x

    @property
    def y(self):
        return self.hitbox.top

    @y.setter
    def y(self, y):
        self.hitbox.top = y

    def update_animation(self, animation_name=None):
        if not animation_name or (self.animation and self.animation.name is animation_name):
            self.animation.next_frame()
        else:
            self.animation.reset()
            self.animation = self.animations[animation_name]

    def get_sprite(self):
        return self.animation.get_current_sprite()

    @property
    def image_x(self):
        return self.x + self.image_offset[0]

    @property
    def image_y(self):
        return self.y + self.image_offset[1]


class Controls:
    up = pygame.K_w
    left = pygame.K_a
    right = pygame.K_d


class Player(GameObject):
    drag = 0.03

    def __init__(self,
                 initial_pos=(0, 0),
                 initial_vel=(0, 0),
                 initial_animation="neutral"):
        super().__init__(hitbox=pygame.Rect(initial_pos[0], initial_pos[1], 20, 48),
                         initial_vel=initial_vel,
                         move_speed=7,
                         animations=asset_factory.load_player_animations(),
                         initial_animation=initial_animation,
                         image_offset=(-23, -5))
        self.jetpack_power = 5.5
        self.in_air = False

    def update_velocity(self, inputs, dt):
        if inputs[Controls.up]:
            self.y_vel -= dt * self.jetpack_power
            self.in_air = True

        self.y_vel = self.y_vel + dt * GameObject.gravity
        self.y_vel -= self.drag * self.y_vel * dt

        if self.in_air:
            x_accel_sum = 0
            if inputs[Controls.left]:
                x_accel_sum -= dt * self.jetpack_power / 3
            if inputs[Controls.right]:
                x_accel_sum += dt * self.jetpack_power / 3
            self.x_vel += x_accel_sum
            self.x_vel -= self.drag * self.x_vel * dt
        else:
            x_vel_sum = 0
            if inputs[Controls.left]:
                x_vel_sum -= self.move_speed
            if inputs[Controls.right]:
                x_vel_sum += self.move_speed
            self.x_vel = x_vel_sum
