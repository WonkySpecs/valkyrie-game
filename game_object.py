class GameObject(object):
    def __init__(self, initial_pos=(0, 0), initial_vel=(0, 0), animations=None, initial_animation="neutral"):
        self.x, self.y = initial_pos
        self.x_vel, self.y_vel = initial_vel
        self.animations = animations
        self.animation_timer = 0
        self.animation = animations[initial_animation]

    def update_animation(self, animation_name=None):
        if not animation_name or (self.animation and self.animation.name is animation_name):
            self.animation.next_frame()
        else:
            self.animation.reset()
            self.animation = self.animations[animation_name]

    def get_sprite(self):
        return self.animation.get_current_sprite()
