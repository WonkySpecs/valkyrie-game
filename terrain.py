from game_objects import SingleSprite


class Terrain(SingleSprite):
    def __init__(self, animations, initial_pos, initial_animation='neutral', platform=False):
        super().__init__(initial_pos=initial_pos,
                         animations=animations,
                         initial_animation=initial_animation)
        self.block_object = self.platform_block if platform else self.standard_block

    def take_damage(self, proj):
        pass

    def standard_block(self, object, moved_hb):
        hb = object.hitbox
        x_ok = y_ok = in_air = True
        if self.hitbox.top < hb.bottom and self.hitbox.bottom > hb.top:
            if object.x_vel > 0 and moved_hb.left < self.hitbox.left <= moved_hb.right:
                moved_hb.right = self.hitbox.left
                x_ok = False
            elif object.x_vel < 0 and moved_hb.right > self.hitbox.right >= moved_hb.left:
                moved_hb.left = self.hitbox.right
                x_ok = False

        if self.hitbox.left < hb.right and self.hitbox.right > hb.left:
            if object.y_vel > 0 and moved_hb.top < self.hitbox.top <= moved_hb.bottom:
                moved_hb.bottom = self.hitbox.top
                y_ok = False
                in_air = False
            elif object.y_vel < 0 and moved_hb.bottom > self.hitbox.bottom > moved_hb.top:
                moved_hb.top = self.hitbox.bottom
                y_ok = False

        return x_ok, y_ok, in_air

    def platform_block(self, object, moved_hb):
        hb = object.hitbox
        x_ok = y_ok = in_air = True

        dropping = False
        try:
            dropping = object.force_dropping
        except AttributeError:
            pass

        if self.hitbox.left < hb.right and self.hitbox.right > hb.left:
            if object.y_vel > 0 \
                    and not dropping \
                    and not object.hitbox.bottom > self.hitbox.bottom \
                    and moved_hb.top < self.hitbox.top <= moved_hb.bottom:
                moved_hb.bottom = self.hitbox.top
                y_ok = False
                in_air = False

        return x_ok, y_ok, in_air
