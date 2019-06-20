import pygame
from game_objects import Player
from asset_factory import load_player_animations, get_background

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

MAX_FPS = 60
EXPECTED_FRAME_TIME_MS = 17

DEBUG = True


def update(game_state):
    player = game_state["player"]

    pressed = pygame.key.get_pressed()
    dt = game_state['clock'].tick(MAX_FPS)
    frac_expected_time_passed = dt / EXPECTED_FRAME_TIME_MS
    in_air = player.y < game_state['player_boundaries'][0].bottom - 64
    player.update_velocity(pressed, frac_expected_time_passed, in_air)

    current_player_animation = "neutral"
    if player.flying:
        if pressed[pygame.K_a]:
            current_player_animation = "fly_left"
        elif pressed[pygame.K_d]:
            current_player_animation = "fly_right"
        else:
            current_player_animation = "fly_neutral"
    player.update_animation(current_player_animation)

    if pygame.mouse.get_pressed()[0]:
        # Gives pos in screen, need to convert to world. Tough with moving camera center :/
        print(pygame.mouse.get_pos())

    new_x = player.x + frac_expected_time_passed * player.x_vel
    new_y = player.y + frac_expected_time_passed * player.y_vel
    bound = game_state["player_boundaries"][0]
    moved_x_hitbox = player.hitbox.copy()
    moved_x_hitbox.left = new_x
    # TODO: Set edge of hitbox properly. Convert bounds to be like terrain objects
    if bound.contains(moved_x_hitbox):
        player.x = new_x
    else:
        player.x_vel = 0

    moved_y_hitbox = player.hitbox.copy()
    moved_y_hitbox.top = new_y
    if bound.contains(moved_y_hitbox):
        player.y = new_y
    else:
        player.y_vel = 0


def get_screen_coordinate(screen_center, camera_center, point):
    offset_x, offset_y = screen_center.x - camera_center.x, screen_center.y - camera_center.y
    return point.x + offset_x, point.y + offset_y


def rect_to_pointlist(rect, coordinate_convert_func):
    corners = [(rect.left, rect.top), (rect.right, rect.top),
               (rect.right, rect.bottom), (rect.left, rect.bottom)]
    return [coordinate_convert_func(pygame.Vector2(corner)) for corner in corners]


def draw(screen, game_state):
    player = game_state["player"]
    screen_center = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    camera_center = pygame.math.Vector2(player.x, player.y - 80)

    def calc_screen_position(point):
        return get_screen_coordinate(screen_center, camera_center, point)

    screen.fill((123, 123, 123))
    for bg_image, bg_top_left in game_state["backgrounds"]:
        screen.blit(bg_image, calc_screen_position(bg_top_left))

    screen.blit(player.get_sprite(), calc_screen_position(pygame.Vector2(player.image_x, player.image_y)))

    if DEBUG:
        pygame.draw.polygon(screen, (255, 0, 0), rect_to_pointlist(player.hitbox, calc_screen_position), 1)
        for bound in game_state['player_boundaries']:
            pygame.draw.polygon(screen, (255, 0, 0), rect_to_pointlist(bound, calc_screen_position), 2)
    fps = game_state['hud_font'].render(f"{game_state['clock'].get_fps():.2f} fps", True, (0, 255, 0))
    screen.blit(fps, (0, 0))
    pygame.display.update()


def main():
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Valkyrie")
    bg_sprite = get_background()
    clock = pygame.time.Clock()
    game_state = {
        "player": Player(initial_pos=(1, 1),
                         initial_vel=(0, 0),
                         animations=load_player_animations()),
        "backgrounds": [(bg_sprite, pygame.Vector2(-350, -300))],
        "buttons_held": [],
        "player_boundaries": [pygame.Rect(0, 0, 1200, 900)],
        "clock": clock,
        "hud_font": pygame.font.Font(None, 20)
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
