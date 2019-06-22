import os
from pygame import image, transform
from animation import Animation

_asset_root_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bin")
_sprite_folder = "sprites"


def load_sprite(sprite_file_name, extension="png"):
    return image.load(os.path.join(_asset_root_folder, _sprite_folder, sprite_file_name + "." + extension)).convert_alpha()


def load_player_animations():
    flight_sprites = [load_sprite("player_neutral_flight_1"),
                      load_sprite("player_neutral_flight_2"),
                      load_sprite("player_neutral_flight_3")]
    durations = [18 for _ in range(len(flight_sprites))]
    animations = [Animation('neutral', [load_sprite("player_neutral")], [1234], [(-23, -5)]),
                  Animation('fly_neutral', flight_sprites, durations, [(-23, -5)]),
                  Animation('fly_left', [transform.rotate(s, 20) for s in flight_sprites], durations, [(-30, -15)]),
                  Animation('fly_right', [transform.rotate(s, -20) for s in flight_sprites], durations, [(-25, -15)])]
    return {
        a.name: a for a in animations
    }


def get_background():
    return transform.scale(image.load(os.path.join(_asset_root_folder, "bg.jpg")).convert_alpha(), (1600, 1200))


def wall_animation(width, height):
    return {'neutral': Animation('neutral', [transform.scale(load_sprite("black"), (width, height))], [1000])}


def assault_soldier_green():
    neutral = load_sprite("assault_soldier_neutral")
    return {'face_right': Animation('face_right', [neutral], [1234], [(-12, -9)]),
            'face_left': Animation('face_left', [transform.flip(neutral, True, False)], [1234], [(-27, -9)])}
