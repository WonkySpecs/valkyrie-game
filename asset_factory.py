import os
from pygame import image, transform, Vector2
from animation import Animation

_asset_root_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bin")
_sprites_to_load = [
    'player_neutral_flight_1',
    'player_neutral_flight_2',
    'player_neutral_flight_3',
    'player_neutral',
    'assault_soldier_neutral',
    'black',
    'yellow_bullet',
    'worm_head_1',
    'worm_head_2',
    'worm_segment'
]


class AssetFactory:
    def __init__(self):
        self._loaded_sprites = {}
        self.load_sprites(_sprites_to_load)

    def load_sprites(self, sprite_names):
        for name in sprite_names:
            self._loaded_sprites[name] = AssetFactory._load_sprite(name)

    @staticmethod
    def _load_sprite(sprite_file_name, extension="png"):
        return image.load(
            os.path.join(_asset_root_folder, "sprites", sprite_file_name + "." + extension)).convert_alpha()

    def get_sprite(self, name):
        if name not in self._loaded_sprites:
            self._load_sprite(name)
        return self._loaded_sprites[name].copy()

    def player_animations(self):
        flight_sprites = [self.get_sprite("player_neutral_flight_1"),
                          self.get_sprite("player_neutral_flight_2"),
                          self.get_sprite("player_neutral_flight_3")]
        durations = [18 for _ in range(len(flight_sprites))]
        animations = [Animation(name='neutral',
                                frames=[self.get_sprite("player_neutral")],
                                durations=[1234],
                                hitbox_size=Vector2(18, 48),
                                offsets=[Vector2(-25, -5)]),
                      Animation(name='fly_neutral',
                                frames=flight_sprites,
                                durations=durations,
                                hitbox_size=Vector2(18, 48),
                                offsets=[(-25, -5) for _ in flight_sprites]),
                      Animation(name='fly_left',
                                frames=[transform.rotate(s, 20) for s in flight_sprites],
                                durations=durations,
                                hitbox_size=Vector2(25, 48),
                                offsets=[Vector2(-29, -15) for _ in flight_sprites]),
                      Animation(name='fly_right',
                                frames=[transform.rotate(s, -20) for s in flight_sprites],
                                durations=durations,
                                hitbox_size=Vector2(25, 48),
                                offsets=[Vector2(-28, -15) for _ in flight_sprites])]
        return {
            a.name: a for a in animations
        }

    def get_background(self):
        return transform.scale(image.load(os.path.join(_asset_root_folder, "bg.jpg")).convert_alpha(), (1600, 1200))

    def wall_animation(self, width, height):
        return {'neutral': Animation('neutral',
                                     [transform.scale(self.get_sprite("black"), (width, height))],
                                     [1000],
                                     Vector2(width, height))}

    def assault_soldier_green(self):
        neutral = self.get_sprite("assault_soldier_neutral")
        return {'face_right': Animation(name='face_right',
                                        frames=[neutral],
                                        durations=[1234],
                                        hitbox_size=Vector2(24, 50),
                                        offsets=[Vector2(-12, -9)]),
                'face_left': Animation(name='face_left',
                                       frames=[transform.flip(neutral, True, False)],
                                       durations=[1234],
                                       hitbox_size=Vector2(24, 50),
                                       offsets=[Vector2(-27, -9)])}

    def yellow_bullet(self):
        return {'neutral': Animation('neutral', [self.get_sprite('yellow_bullet')], [1000], Vector2(3, 3))}

    # def worm(self):
    #     head_sprites = [self.get_sprite('worm_head_1'), self.get_sprite('worm_head_2')]
    #     head_durations = [25 for _ in head_sprites]
    #     animations = [Animation('head_up', head_sprites, head_durations),
    #                   Animation('head_right', [transform.rotate(s, -90) for s in head_sprites], head_durations),
    #                   Animation('head_down', [transform.rotate(s, 180) for s in head_sprites], head_durations),
    #                   Animation('head_left', [transform.rotate(s, 90) for s in head_sprites], head_durations),
    #                   Animation('segment', [self.get_sprite('worm_segment')], [1000])]
    #     return {a.name: a for a in animations}
