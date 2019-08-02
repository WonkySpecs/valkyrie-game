import pygame
from typing import List, Tuple, Callable

from valkyrie import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG


def get_screen_coordinate(screen_center: pygame.Vector2,
                          camera_center: pygame.Vector2,
                          point: pygame.Vector2) -> Tuple[int, int]:
    offset_x, offset_y = screen_center.x - camera_center.x, screen_center.y - camera_center.y
    return point.x + offset_x, point.y + offset_y


def rect_to_pointlist(rect: pygame.rect,
                      coordinate_convert_func: Callable[[pygame.Vector2], Tuple[int, int]]
                      ) -> List[Tuple[int, int]]:
    corners = [(rect.left, rect.top), (rect.right, rect.top),
               (rect.right, rect.bottom), (rect.left, rect.bottom)]
    return [coordinate_convert_func(pygame.Vector2(corner)) for corner in corners]


def draw(screen, game_state):
    player = game_state.player
    screen_center = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    camera_center = pygame.math.Vector2(player.x, player.y)
    game_state.last_camera_center = camera_center

    def calc_screen_position(point: pygame.Vector2) -> Tuple[int, int]:
        return get_screen_coordinate(screen_center, camera_center, point)

    screen.fill((123, 123, 123))

    for z in sorted(game_state.background_layers.keys()):
        for bg_image, bg_top_left in game_state.background_layers[z]:
            screen.blit(bg_image, calc_screen_position(bg_top_left))

    for terrain in game_state.terrain:
        terrain.draw(screen, calc_screen_position)

    for enemy in game_state.enemies:
        enemy.draw(screen, calc_screen_position)

    for enemy_proj in game_state.enemy_projectiles:
        enemy_proj.draw(screen, calc_screen_position)

    player.draw(screen, calc_screen_position)

    for projectile in game_state.player_projectiles:
        projectile.draw(screen, calc_screen_position)

    if DEBUG:
        pygame.draw.polygon(screen, (0, 255, 0), rect_to_pointlist(player.hitbox, calc_screen_position), 1)
        for enemy in game_state.enemies:
            pygame.draw.polygon(screen, (255, 0, 0), rect_to_pointlist(enemy.hitbox, calc_screen_position), 1)

    fps = game_state.hud['font'].render(f"{game_state.clock.get_fps():.2f} fps", True, (0, 255, 0))
    screen.blit(fps, (0, 0))
    pygame.display.update()
