import os
import pygame
from animation import Animation

_asset_root_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bin")
_sprite_folder = "sprites"


def load_sprite(sprite_file_name, extension="png"):
    return pygame.image.load(os.path.join(_asset_root_folder, _sprite_folder, sprite_file_name + "." + extension)).convert_alpha()


def load_player_animations():
    flight_sprites = [load_sprite("player_neutral_flight_1"),
                      load_sprite("player_neutral_flight_2"),
                      load_sprite("player_neutral_flight_3")]
    durations = [18 for _ in range(len(flight_sprites))]
    animations = [Animation('neutral', [load_sprite("player_neutral")], [1234]),
                  Animation('fly_neutral', flight_sprites, durations),
                  Animation('fly_left', [pygame.transform.rotate(s, 20) for s in flight_sprites], durations),
                  Animation('fly_right', [pygame.transform.rotate(s, -20) for s in flight_sprites], durations)]
    return {
        a.name: a for a in animations
    }


def get_background():
    return pygame.transform.scale(pygame.image.load(os.path.join(_asset_root_folder, "bg.jpg")).convert_alpha(), (1600, 1200))


def wall_animation(width, height):
    return {'neutral': Animation('neutral', [pygame.transform.scale(load_sprite("black"), (width, height))], [1000])}


def assault_soldier_green():
    return {'neutral': Animation('neutral', [load_sprite("assault_soldier_neutral")], [1234])}
