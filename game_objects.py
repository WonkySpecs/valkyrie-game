import pygame
import asset_factory


class GameObject:
    gravity = 2.3

    def __init__(self, hitbox=None, initial_vel=(0, 0), move_speed=0, drag=0.03,
                 animations=None, initial_animation="neutral", image_offset=(0, 0)):
        self.hitbox = hitbox
        self._exact_pos = pygame.Vector2(hitbox.left, hitbox.top)
        self.x_vel, self.y_vel = initial_vel
        self.move_speed = move_speed
        self.animations = animations
        self.animation_timer = 0
        self.animation = animations[initial_animation]
        self.image_offset = image_offset
        self.in_air = False
        self.drag = drag

    @property
    def x(self):
        return self._exact_pos.x

    @x.setter
    def x(self, x):
        self._exact_pos.x = x
        self.hitbox.left = round(x)

    @property
    def y(self):
        return self._exact_pos.y

    @y.setter
    def y(self, y):
        self._exact_pos.y = y
        self.hitbox.top = round(y)

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

    def update_pos(self, dt, terrain):
        new_x = self.x + dt * self.x_vel
        new_y = self.y + dt * self.y_vel
        moved_x_hb = self.hitbox.copy()
        moved_x_hb.x = new_x

        moved_y_hb = self.hitbox.copy()
        moved_y_hb.y = new_y

        x_ok, y_ok = True, True

        for hb in [terrain_object.hitbox for terrain_object in terrain]:
            if hb.top < self.hitbox.bottom and hb.bottom > self.hitbox.top:
                if moved_x_hb.left < hb.left <= moved_x_hb.right:
                    self.hitbox.right = hb.left
                    self.x_vel = 0
                    x_ok = False
                elif moved_x_hb.right > hb.right >= moved_x_hb.left:
                    self.hitbox.left = hb.right
                    self.x_vel = 0
                    x_ok = False

            if hb.left < self.hitbox.right and hb.right > self.hitbox.left:
                if moved_y_hb.top < hb.top <= moved_y_hb.bottom:
                    self.hitbox.bottom = hb.top
                    self.y_vel = 0
                    self.in_air = False
                    y_ok = False
                elif moved_y_hb.bottom > hb.bottom > moved_y_hb.top:
                    self.hitbox.top = hb.bottom
                    self.y_vel = 0
                    y_ok = False
        if x_ok:
            self.x = new_x
        if y_ok:
            self.y = new_y


class Controls:
    up = pygame.K_w
    left = pygame.K_a
    right = pygame.K_d


class Player(GameObject):
    def __init__(self,
                 initial_pos=(0, 0),
                 initial_vel=(0, 0),
                 initial_animation="neutral"):
        super().__init__(hitbox=pygame.Rect(initial_pos[0], initial_pos[1], 20, 48),
                         initial_vel=initial_vel,
                         move_speed=7,
                         animations=asset_factory.load_player_animations(),
                         initial_animation=initial_animation,
                         image_offset=(-23, -5),
                         drag=0.03)
        self.jetpack_power = 5.5

    def update(self, pressed, dt, terrain):
        self.update_velocity(pressed, dt)

        current_player_animation = "neutral"
        if self.in_air:
            if pressed[pygame.K_a]:
                current_player_animation = "fly_left"
            elif pressed[pygame.K_d]:
                current_player_animation = "fly_right"
            elif pressed[pygame.K_w]:
                current_player_animation = "fly_neutral"
        self.update_animation(current_player_animation)
        self.update_pos(dt, terrain)

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
