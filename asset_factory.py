import os
from enum import Enum, auto
from pygame import image


class Entity(Enum):
    BACKGROUND = auto()
    PLAYER = auto()


_asset_root_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bin")
_sprite_folder = "sprites"

something = {
    Entity.PLAYER: os.path.join(_sprite_folder, "player_neutral.png"),
    Entity.BACKGROUND: "bg.jpg"
}

def get_sprite(entity):
    return image.load(os.path.join(_asset_root_folder, something[entity]))