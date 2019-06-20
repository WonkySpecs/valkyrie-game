import pygame


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


class Player(GameObject):
    drag = 0.03

    def __init__(self,
                 initial_pos=(0, 0),
                 initial_vel=(0, 0),
                 animations=None,
                 initial_animation="neutral"):
        super().__init__(hitbox=pygame.Rect(initial_pos[0], initial_pos[1], 20, 48),
                         initial_vel=initial_vel,
                         move_speed=7,
                         animations=animations,
                         initial_animation=initial_animation,
                         image_offset=(-23, -5))
        self.jetpack_power = 5.5
        self.flying = False

    def update_velocity(self, inputs, dt, in_air=False):
        if inputs[pygame.K_w]:
            self.y_vel -= dt * self.jetpack_power
        self.flying = inputs[pygame.K_w] or (
                in_air and (
                    inputs[pygame.K_a] or inputs[pygame.K_d]))
        if self.flying:
            if inputs[pygame.K_a]:
                self.x_vel -= dt * self.jetpack_power / 3
            elif inputs[pygame.K_d]:
                self.x_vel += dt * self.jetpack_power / 3
        else:
            if not in_air:
                if inputs[pygame.K_a]:
                    self.x_vel = -self.move_speed
                elif inputs[pygame.K_d]:
                    self.x_vel = self.move_speed
                else:
                    self.x_vel = 0
        self.y_vel = self.y_vel + dt * GameObject.gravity

        self.x_vel -= self.drag * self.x_vel * dt
        self.y_vel -= self.drag * self.y_vel * dt
