import os
from pygame import image, transform

_asset_root_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bin")
_sprite_folder = "sprites"


def load_sprite(sprite_file_name, extension="png"):
    return image.load(os.path.join(_asset_root_folder, _sprite_folder, sprite_file_name + "." + extension))


def get_player_sprites():
    flight_sprites = [load_sprite("player_neutral_flight_1"),
                      load_sprite("player_neutral_flight_2"),
                      load_sprite("player_neutral_flight_3")]
    return {
        'neutral': [load_sprite("player_neutral")],
        'fly_neutral': flight_sprites,
        'fly_left': [transform.rotate(s, 20) for s in flight_sprites],
        'fly_right': [transform.rotate(s, -20) for s in flight_sprites]
    }


def get_background():
    return image.load(os.path.join(_asset_root_folder, "bg.jpg"))
