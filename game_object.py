class GameObject(object):
    def __init__(self, initial_pos=(0, 0), initial_vel=(0, 0), sprites=None):
        self.x, self.y = initial_pos
        self.x_vel, self.y_vel = initial_vel
        self.sprites = sprites
        self.animation = "neutral"
        self.animation_timer = 0

    def update_animation(self, animation):
        if self.animation is animation:
            self.animation_timer = (self.animation_timer + 1) % 47
        else:
            self.animation = animation
            self.animation_timer = 0

    def get_sprite(self):
        return self.sprites[self.animation][self.animation_timer // (48 // len(self.sprites[self.animation]))]
