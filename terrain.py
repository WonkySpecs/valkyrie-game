from game_objects import SingleSprite


class Terrain(SingleSprite):
    def __init__(self, animations, initial_pos, initial_animation='neutral', platform=False):
        super().__init__(initial_pos=initial_pos,
                         animations=animations,
                         initial_animation=initial_animation)
        self.block_object = self.platform_block if platform else self.standard_block

    def take_damage(self, proj):
        pass

    def standard_block(self, object, moved_x_hb, moved_y_hb):
        hb = object.hitbox
        x_ok = y_ok = in_air = True
        if self.hitbox.top < hb.bottom and self.hitbox.bottom > hb.top:
            if object.x_vel > 0 and moved_x_hb.left < self.hitbox.left <= moved_x_hb.right:
                moved_x_hb.right = self.hitbox.left
                x_ok = False
            elif object.x_vel < 0 and moved_x_hb.right > self.hitbox.right >= moved_x_hb.left:
                moved_y_hb.left = self.hitbox.right
                x_ok = False

        if self.hitbox.left < hb.right and self.hitbox.right > hb.left:
            if object.y_vel > 0 and moved_y_hb.top < self.hitbox.top <= moved_y_hb.bottom:
                moved_y_hb.bottom = self.hitbox.top
                y_ok = False
                in_air = False
            elif object.y_vel < 0 and moved_y_hb.bottom > self.hitbox.bottom > moved_y_hb.top:
                moved_y_hb.top = self.hitbox.bottom
                y_ok = False

        return x_ok, y_ok, in_air

    def platform_block(self, object, moved_x_hb, moved_y_hb):
        pass
