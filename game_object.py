class GameObject(object):
    def __init__(self, initial_pos=(0, 0), initial_vel=(0, 0), sprites=None):
        self.x, self.y = initial_pos
        self.x_vel, self.y_vel = initial_vel
        self.sprites = sprites

    def get_sprite(self):
        return self.sprites['neutral'][0]
