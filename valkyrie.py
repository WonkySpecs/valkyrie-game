import pygame
from game_objects import GameObject, Player
import enemy_classes
from asset_factory import AssetFactory

import random
import math

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

MAX_FPS = 500

DEBUG = True

x = 0


def update(game_state):
    player = game_state["player"]

    pressed = pygame.key.get_pressed()
    dt = game_state['clock'].tick(MAX_FPS) / 30

    player.update(pressed, dt, game_state['terrain'])
    global x
    x += 1

    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        offset = pygame.Vector2(mx - SCREEN_WIDTH // 2, my - SCREEN_HEIGHT // 2)
        mouse_world_pos = game_state['last_camera_center'] + offset
        if x > 100:
            game_state['enemies'].append(enemy_classes.Worm(initial_pos=(mouse_world_pos.x, mouse_world_pos.y),
                                                            animations=AssetFactory().worm()))
            x = 0
        new_proj = player.shoot_at(mouse_world_pos)
        if new_proj:
            game_state['player_projectiles'].append(new_proj)

    for enemy in game_state['enemies']:
        enemy.update(dt, game_state['terrain'], (player.x, player.y))

    for proj in game_state['player_projectiles']:
        proj.update_pos(dt, terrain=[])


def main():
    from drawing import draw
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Valkyrie")
    assets = AssetFactory()
    bg_sprite = assets.get_background()
    clock = pygame.time.Clock()
    terrain = [GameObject(pygame.Rect(-200, 0, 900, 50), animations=assets.wall_animation(900, 50)),
               GameObject(pygame.Rect(-200, 800, 900, 15), animations=assets.wall_animation(900, 15)),
               GameObject(pygame.Rect(-200, 0, 20, 800), animations=assets.wall_animation(20, 800)),
               GameObject(pygame.Rect(700, 0, 50, 800), animations=assets.wall_animation(50, 800)),
               GameObject(pygame.Rect(300, 300, 50, 50), animations=assets.wall_animation(50, 50))]

    def fire_gun(target_pos, start_pos):
        h = target_pos - start_pos
        theta = math.atan2(h.y, h.x)
        x_vel = 40 * math.cos(theta)
        y_vel = 40 * math.sin(theta)
        return GameObject(hitbox=pygame.Rect(start_pos.x, start_pos.y, 3, 3),
                          initial_vel=(x_vel, y_vel),
                          animations=assets.yellow_bullet())

    game_state = {
        "player": Player(initial_pos=(320, 50), animations=assets.player_animations(), fire_gun=fire_gun),
        "enemies": [*[enemy_classes.AssaultSoldier((50 + x, 500),
                                                   (0, -30),
                                                   move_speed=random.randint(-5, 5),
                                                   animations=assets.assault_soldier_green())
                      for x in range(50, 600, 25)],
                    enemy_classes.Worm(initial_pos=(0, 500), animations=assets.worm())],
        "player_projectiles": [],
        "enemy_projectiles": [],
        "backgrounds": [(bg_sprite, pygame.Vector2(-350, -300))],
        "buttons_held": [],
        "terrain": terrain,
        "clock": clock,
        "hud_font": pygame.font.Font(None, 20),
        "last_camera_center": None
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

        update(game_state)
        draw(window, game_state)
    pygame.quit()


if __name__ == "__main__":
    main()
