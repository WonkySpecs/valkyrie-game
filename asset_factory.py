import os
from pygame import image, transform
from animation import Animation

_asset_root_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bin")
_sprites_to_load = [
    'player_neutral_flight_1',
    'player_neutral_flight_2',
    'player_neutral_flight_3',
    'player_neutral',
    'assault_soldier_neutral',
    'black',
    'yellow_pixel'
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
        animations = [Animation('neutral', [self.get_sprite("player_neutral")], [1234], [(-23, -5)]),
                      Animation('fly_neutral', flight_sprites, durations, [(-23, -5)]),
                      Animation('fly_left', [transform.rotate(s, 20) for s in flight_sprites], durations, [(-30, -15)]),
                      Animation('fly_right', [transform.rotate(s, -20) for s in flight_sprites], durations,
                                [(-25, -15)])]
        return {
            a.name: a for a in animations
        }

    def get_background(self):
        return transform.scale(image.load(os.path.join(_asset_root_folder, "bg.jpg")).convert_alpha(), (1600, 1200))

    def wall_animation(self, width, height):
        return {'neutral': Animation('neutral', [transform.scale(self.get_sprite("black"), (width, height))], [1000])}

    def assault_soldier_green(self):
        neutral = self.get_sprite("assault_soldier_neutral")
        return {'face_right': Animation('face_right', [neutral], [1234], [(-12, -9)]),
                'face_left': Animation('face_left', [transform.flip(neutral, True, False)], [1234], [(-27, -9)])}
