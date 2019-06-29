import pygame
from game_objects import GameObject, Player
import enemy_classes
from asset_factory import AssetFactory
from game_state import GameState

import random
import math

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

MAX_FPS = 500

DEBUG = True


def update(game_state):
    player = game_state.player

    pressed = pygame.key.get_pressed()
    dt = game_state.clock.tick(MAX_FPS) / 30

    player.update(pressed, dt, game_state.terrain)

    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        offset = pygame.Vector2(mx - SCREEN_WIDTH // 2, my - SCREEN_HEIGHT // 2)
        mouse_world_pos = game_state.last_camera_center + offset
        new_proj = player.shoot_at(mouse_world_pos)
        if new_proj:
            game_state.player_projectiles.append(new_proj)

    for enemy in game_state.enemies:
        enemy.update(dt, game_state.terrain, (player.x, player.y))

    for proj in game_state.player_projectiles:
        proj.update_pos(dt, terrain=game_state.terrain)


def main():
    from drawing import draw
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Valkyrie")
    assets = AssetFactory()
    bg_sprite = assets.get_background()
    terrain = [GameObject(pygame.Rect(-200, 0, 900, 50), animations=assets.wall_animation(900, 50)),
               GameObject(pygame.Rect(-200, 800, 900, 15), animations=assets.wall_animation(900, 15)),
               GameObject(pygame.Rect(-200, 0, 20, 800), animations=assets.wall_animation(20, 800)),
               GameObject(pygame.Rect(700, 0, 50, 800), animations=assets.wall_animation(50, 800)),
               GameObject(pygame.Rect(300, 300, 50, 50), animations=assets.wall_animation(50, 50))]

    def fire_gun(target_pos, start_pos):
        d_pos = target_pos - start_pos
        theta = math.atan2(d_pos.y, d_pos.x)
        x_vel = 40 * math.cos(theta)
        y_vel = 40 * math.sin(theta)
        return GameObject(hitbox=pygame.Rect(start_pos.x, start_pos.y, 3, 3),
                          initial_vel=(x_vel, y_vel),
                          animations=assets.yellow_bullet())

    state = GameState(
        player=Player(initial_pos=(320, 50), animations=assets.player_animations(), fire_gun=fire_gun),
        enemies=[*[enemy_classes.AssaultSoldier((50 + x, 500),
                                                (0, -30),
                                                move_speed=random.randint(-5, 5),
                                                animations=assets.assault_soldier_green())
                   for x in range(50, 600, 25)]],
        terrain=terrain,
        background_layers={0: [(bg_sprite, pygame.Vector2(-350, -300))]},
        clock=pygame.time.Clock(),
        hud={'font': pygame.font.Font(None, 20)}
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

        update(state)
        draw(window, state)
    pygame.quit()


if __name__ == "__main__":
    main()
