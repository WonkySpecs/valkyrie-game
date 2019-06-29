import pygame

gravity = 2.3


class Sprite:
    def __init__(self,
                 animations,
                 initial_pos=pygame.Vector2(0, 0),
                 initial_animation='neutral'):
        self.animations = animations
        self.animation = self.animations[initial_animation]
        self.image_pos = initial_pos
        self.hitbox = pygame.Rect(self.image_pos, self.animation.hitbox_size)
        self._exact_pos = [initial_pos.x, initial_pos.y]

    def update(self, dt, animation_name=None):
        if not animation_name or (self.animation and self.animation.name is animation_name):
            self.animation.next_frame()
        else:
            self.animation.reset()
            self.animation = self.animations[animation_name]
            self.hitbox = pygame.Rect(self.image_pos, self.animation.hitbox_size)

    def get_sprite(self):
        return self.animation.get_current_sprite(), self.image_pos + self.animation.image_offset

    @property
    def x(self):
        return self._exact_pos[0]

    @x.setter
    def x(self, x):
        self._exact_pos[0] = x
        self.hitbox.left = self.image_pos.x = round(x)

    @property
    def y(self):
        return self._exact_pos[1]

    @y.setter
    def y(self, y):
        self._exact_pos[1] = y
        self.hitbox.top = self.image_pos.y = round(y)


class Controls:
    up = pygame.K_w
    left = pygame.K_a
    right = pygame.K_d


class Player:
    def __init__(self,
                 initial_pos=(0, 0),
                 initial_vel=(0, 0),
                 animations=None,
                 initial_animation="neutral",
                 fire_gun=None):
        self.sprite = Sprite(animations=animations,
                             initial_pos=initial_pos,
                             initial_animation=initial_animation)
        self.x_vel, self.y_vel = initial_vel
        self.jetpack_power = 5.5
        self.shoot_delay = 2
        self.till_next_shot = 0
        self.fire_gun = fire_gun
        self.drag = 0.03
        self.in_air = False
        self.move_speed = 7

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
        self.sprite.update(dt, current_player_animation)
        self.update_pos(dt, terrain)
        self.till_next_shot -= dt

    def update_velocity(self, inputs, dt):
        if inputs[Controls.up]:
            self.y_vel -= dt * self.jetpack_power
            self.in_air = True
        self.y_vel = self.y_vel + dt * gravity
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

    def shoot_at(self, target_pos):
        if self.till_next_shot <= 0:
            self.till_next_shot = self.shoot_delay
            return self.fire_gun(target_pos, pygame.Vector2(self.sprite.x + 32, self.sprite.y + 34))

    def draw(self, surface, coordinate_map):
        image, pos = self.sprite.get_sprite()
        surface.blit(image, coordinate_map(pos))

    @property
    def x(self):
        return self.sprite.x

    @property
    def y(self):
        return self.sprite.y

    @property
    def hitbox(self):
        return self.sprite.hitbox


class Projectile(Sprite):
    def __init__(self, animations, initial_pos, initial_vel):
        super().__init__(animations, initial_pos=initial_pos)
        self.x_vel = initial_vel.x
        self.y_vel = initial_vel.y

    def update(self, dt, terrain):
        super().update(dt)
        self.x += self.x_vel * dt
        self.y += self.y_vel * dt

        for t in terrain:
            if t.hitbox.colliderect(self.hitbox):
                print("Hit wall")

    def draw(self, surface, coordinate_map):
        image, pos = self.get_sprite()
        surface.blit(image, coordinate_map(pos))
