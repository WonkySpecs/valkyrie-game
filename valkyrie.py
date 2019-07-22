import pygame
from asset_factory import AssetFactory
from levels import Level

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

MAX_FPS = 500

DEBUG = True


def cutscene_update(game_state):
    if game_state.cutscene_timer > 50:
        game_state.in_cutscene = False


def update(game_state, level_update):
    dt = game_state.clock.tick(MAX_FPS) / 30
    level_update(dt, game_state)
    game_state.remove_to_remove_objects()

    if game_state.in_cutscene:
        cutscene_update(game_state)
    else:
        player = game_state.player
        pressed = pygame.key.get_pressed()
        player.update(pressed, dt, game_state.terrain)

        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            offset = pygame.Vector2(mx - SCREEN_WIDTH // 2, my - SCREEN_HEIGHT // 2)
            mouse_world_pos = game_state.last_camera_center + offset
            new_proj = player.shoot_at(mouse_world_pos)
            if new_proj:
                game_state.player_projectiles.append(new_proj)

        for enemy in game_state.enemies:
            new_proj = enemy.update(dt, game_state.terrain, pygame.Vector2(player.hitbox.center))
            if new_proj:
                game_state.enemy_projectiles.append(new_proj)

        for proj in game_state.player_projectiles:
            proj.update(dt, *game_state.terrain, *game_state.enemies)

        for enemy_proj in game_state.enemy_projectiles:
            enemy_proj.update(dt, *game_state.terrain, *[game_state.player])


def main():
    from drawing import draw
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Valkyrie")
    level = Level.load(Level.ONE, AssetFactory())
    state = level.initial_game_state

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
        update(state, level.update)
        draw(window, state)
    pygame.quit()


if __name__ == "__main__":
    main()
