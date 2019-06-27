import pygame

from valkyrie import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG


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
        img, pos = terrain_object.get_sprite()
        screen.blit(img, calc_screen_position(pos))

    for enemy in game_state['enemies']:
        screen.blits([(image, calc_screen_position(pos)) for image, pos in enemy.get_sprites()])

    player_img, player_pos = player.get_sprite()
    screen.blit(player_img, calc_screen_position(player_pos))

    for projectile in game_state['player_projectiles']:
        img, pos = projectile.get_sprite()
        screen.blit(img, calc_screen_position(pos))

    if DEBUG:
        pygame.draw.polygon(screen, (0, 255, 0), rect_to_pointlist(player.hitbox, calc_screen_position), 1)
        for enemy in game_state['enemies']:
            pygame.draw.polygon(screen, (255, 0, 0), rect_to_pointlist(enemy.hitbox, calc_screen_position), 1)

    fps = game_state['hud_font'].render(f"{game_state['clock'].get_fps():.2f} fps", True, (0, 255, 0))
    screen.blit(fps, (0, 0))
    pygame.display.update()
