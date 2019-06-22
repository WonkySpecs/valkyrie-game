import pygame
from game_objects import GameObject, Player
import enemy_classes
import asset_factory
import random

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

MAX_FPS = 6000

DEBUG = True

def update(game_state):
    player = game_state["player"]

    pressed = pygame.key.get_pressed()
    dt = game_state['clock'].tick(MAX_FPS) / 20
    player.update(pressed, dt, game_state['terrain'])

    for enemy in game_state['enemies']:
        enemy.update_velocity(dt)
        enemy.update_pos(dt, game_state['terrain'])

    if pygame.mouse.get_pressed()[0]:
        # Gives pos in screen, need to convert to world. Tough with moving camera center :/
        # Camera center will need to be in game_state (needs to be somewhere anyway to know how to move) so can do :)
        print(pygame.mouse.get_pos())


def get_screen_coordinate(screen_center, camera_center, point):
    offset_x, offset_y = screen_center.x - camera_center.x, screen_center.y - camera_center.y
    return point.x + offset_x, point.y + offset_y


def rect_to_pointlist(rect, coordinate_convert_func):
    corners = [(rect.left, rect.top), (rect.right, rect.top),
               (rect.right, rect.bottom), (rect.left, rect.bottom)]
    return [coordinate_convert_func(pygame.Vector2(corner)) for corner in corners]


def aim_camera(last, aim, tracking_speed):
    if not last:
        return aim

    if aim.x > last.x:
        new_aim_x = min(last.x + tracking_speed, aim.x)
    else:
        new_aim_x = max(last.x - tracking_speed, aim.x)

    if aim.y > last.y:
        new_aim_y = min(last.y + tracking_speed, aim.y)
    else:
        new_aim_y = max(last.y - tracking_speed, aim.y)

    return pygame.Vector2(new_aim_x, new_aim_y)


def draw(screen, game_state):
    player = game_state["player"]
    screen_center = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    camera_aim = pygame.math.Vector2(player.x, player.y)
    camera_center = aim_camera(game_state['last_camera_center'], camera_aim, 5)
    game_state['last_camera_center'] = camera_center

    def calc_screen_position(point):
        return get_screen_coordinate(screen_center, camera_center, point)

    screen.fill((123, 123, 123))

    for bg_image, bg_top_left in game_state["backgrounds"]:
        screen.blit(bg_image, calc_screen_position(bg_top_left))

    for terrain_object in game_state['terrain']:
        screen.blit(terrain_object.get_sprite(),
                    calc_screen_position(pygame.Vector2(terrain_object.image_x, terrain_object.image_y)))

    for enemy in game_state['enemies']:
        screen.blit(enemy.get_sprite(), calc_screen_position(pygame.Vector2(enemy.image_x, enemy.image_y)))

    screen.blit(player.get_sprite(), calc_screen_position(pygame.Vector2(player.image_x, player.image_y)))

    if DEBUG:
        pygame.draw.polygon(screen, (0, 255, 0), rect_to_pointlist(player.hitbox, calc_screen_position), 1)
        for enemy in game_state['enemies']:
            pygame.draw.polygon(screen, (255, 0, 0), rect_to_pointlist(enemy.hitbox, calc_screen_position), 1)

    fps = game_state['hud_font'].render(f"{game_state['clock'].get_fps():.2f} fps", True, (0, 255, 0))
    screen.blit(fps, (0, 0))
    pygame.display.update()


def main():
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Valkyrie")
    bg_sprite = asset_factory.get_background()
    clock = pygame.time.Clock()
    terrain = [GameObject(pygame.Rect(-200, 0, 900, 50), animations=asset_factory.wall_animation(900, 50)),
               GameObject(pygame.Rect(-200, 800, 900, 15), animations=asset_factory.wall_animation(900, 15)),
               GameObject(pygame.Rect(-200, 0, 20, 800), animations=asset_factory.wall_animation(20, 800)),
               GameObject(pygame.Rect(700, 0, 50, 800), animations=asset_factory.wall_animation(50, 800)),
               GameObject(pygame.Rect(300, 300, 50, 50), animations=asset_factory.wall_animation(50, 50))]
    game_state = {
        "player": Player(initial_pos=(320, 50)),
        "enemies": [enemy_classes.AssaultSoldier((50 + x, 500), (random.randint(-5, 5), -30)) for x in range(50, 600, 25)],
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
