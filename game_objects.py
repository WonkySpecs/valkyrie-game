import pygame

gravity = 2.3


class VelocityUpdates:
    @staticmethod
    def gravity(self, dt):
        self.y_vel = self.y_vel + dt * gravity

    @staticmethod
    def drag(self, dt):
        self.y_vel -= self.drag * self.y_vel * dt


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
        self.to_remove = False

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


class SingleSprite:
    def __init__(self,
                 animations,
                 initial_pos,
                 initial_animation='neutral'):
        self.sprite = Sprite(animations=animations,
                             initial_pos=initial_pos,
                             initial_animation=initial_animation)
        self.to_remove = False

    def hit_by(self, proj):
        return proj.hitbox.colliderect(self.sprite.hitbox)

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


class BlockedByTerrain(SingleSprite):
    def __init__(self, animations, initial_pos, initial_animation):
        super().__init__(animations, initial_pos, initial_animation)
        self.force_dropping = False

    def update_pos(self, dt, terrain):
        hitbox = self.hitbox
        new_x = self.x + dt * self.x_vel
        new_y = self.y + dt * self.y_vel
        moved_hb = hitbox.copy()
        moved_hb.x = new_x
        moved_hb.y = new_y

        all_x_ok = all_y_ok = all_in_air = True
        for t in terrain:
            x_ok, y_ok, in_air = t.block_object(self, moved_hb)
            all_x_ok = all_x_ok and x_ok
            all_y_ok = all_y_ok and y_ok
            all_in_air = all_in_air and in_air
        self.in_air = all_in_air
        if all_x_ok:
            self.sprite.x = new_x
        else:
            self.x_vel = 0
            self.hitbox.left = self.sprite.x = moved_hb.left

        if all_y_ok:
            self.sprite.y = new_y
        else:
            self.y_vel = 0
            self.hitbox.top = self.sprite.y = moved_hb.top


class Controls:
    up = pygame.K_w
    left = pygame.K_a
    right = pygame.K_d
    down = pygame.K_s


class Player(BlockedByTerrain):
    def __init__(self,
                 initial_pos=(0, 0),
                 initial_vel=(0, 0),
                 animations=None,
                 initial_animation="neutral",
                 fire_gun=None):
        super().__init__(animations=animations,
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
        self.health = 1000

    def update(self, pressed, dt, terrain):
        self.update_velocity(pressed, dt)

        current_player_animation = "neutral"
        if self.in_air:
            if pressed[Controls.left]:
                current_player_animation = "fly_left"
            elif pressed[Controls.right]:
                current_player_animation = "fly_right"
            elif pressed[Controls.up]:
                current_player_animation = "fly_neutral"
        self.sprite.update(dt, current_player_animation)
        self.force_dropping = pressed[Controls.down]
        self.update_pos(dt, terrain)
        self.till_next_shot -= dt

    def update_velocity(self, inputs, dt):
        if inputs[Controls.up]:
            self.y_vel -= dt * self.jetpack_power
            self.in_air = True
        VelocityUpdates.gravity(self, dt)
        VelocityUpdates.drag(self, dt)

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
            return self.fire_gun(target_pos, pygame.Vector2(self.sprite.x + 32, self.sprite.y + 34))

    def take_damage(self, proj):
        self.health -= proj.damage


class Projectile(Sprite):
    def __init__(self,
                 animations,
                 initial_pos,
                 initial_vel,
                 damage):
        super().__init__(animations, initial_pos=initial_pos)
        self.x_vel = initial_vel.x
        self.y_vel = initial_vel.y
        self.damage = damage

    def update(self, dt, *targets):
        super().update(dt)
        self.x += self.x_vel * dt
        self.y += self.y_vel * dt

        for target in targets:
            if target.hit_by(self):
                target.take_damage(self)
                self.to_remove = True
                break

    def draw(self, surface, coordinate_map):
        image, pos = self.get_sprite()
        surface.blit(image, coordinate_map(pos))
