import pygame


class Sprite:
    def __init__(self, animations,
                 initial_animation='neutral',
                 initial_pos=pygame.Vector2(0, 0)):
        self.animations = animations
        self.animation = self.animations[initial_animation]
        self.image_pos = initial_pos

    def update(self, dt, animation_name):
        if not animation_name or (self.animation and self.animation.name is animation_name):
            self.animation.next_frame()
        else:
            self.animation.reset()
            self.animation = self.animations[animation_name]

    def get_sprite(self):
        return self.animation.get_current_sprite(), self.image_pos + self.animation.image_offset


class GameObject(Sprite):
    gravity = 2.3

    def __init__(self,
                 hitbox,
                 animations,
                 initial_vel=(0, 0),
                 move_speed=0,
                 drag=0.03,
                 initial_animation="neutral"):
        super().__init__(animations,
                         initial_animation=initial_animation,
                         initial_pos=pygame.Vector2(hitbox.left, hitbox.top))
        self.hitbox = hitbox
        self._exact_pos = pygame.Vector2(hitbox.left, hitbox.top)
        self.x_vel, self.y_vel = initial_vel
        self.move_speed = move_speed
        self.in_air = False
        self.drag = drag

    @property
    def x(self):
        return self._exact_pos.x

    @x.setter
    def x(self, x):
        self._exact_pos.x = x
        self.hitbox.left = self.image_pos.x = round(x)

    @property
    def y(self):
        return self._exact_pos.y

    @y.setter
    def y(self, y):
        self._exact_pos.y = y
        self.hitbox.top = self.image_pos.y = round(y)

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
                 animations=None,
                 initial_animation="neutral",
                 fire_gun=None):
        super().__init__(hitbox=pygame.Rect(initial_pos[0], initial_pos[1], 20, 48),
                         initial_vel=initial_vel,
                         move_speed=7,
                         animations=animations,
                         initial_animation=initial_animation,
                         drag=0.03)
        self.jetpack_power = 5.5
        self.shoot_delay = 2
        self.till_next_shot = 0
        self.fire_gun = fire_gun

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
        super().update(dt, current_player_animation)
        self.update_pos(dt, terrain)
        self.till_next_shot -= dt

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

    def shoot_at(self, target_pos):
        if self.till_next_shot <= 0:
            self.till_next_shot = self.shoot_delay
            return self.fire_gun(target_pos, pygame.Vector2(self.x + 32, self.y + 34))
