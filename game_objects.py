from pygame import Rect


class GameObject:
    gravity = 0.035

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
    drag_multiplier = 0.05
    terminal_velocity = 6

    def __init__(self,
                 initial_pos=(0, 0),
                 initial_vel=(0, 0),
                 animations=None,
                 initial_animation="neutral"):
        super().__init__(hitbox=Rect(initial_pos[0], initial_pos[1], 20, 48),
                         initial_vel=initial_vel,
                         move_speed=1,
                         animations=animations,
                         initial_animation=initial_animation,
                         image_offset=(-23, -5))
        self.jetpack_power = 0.45
