import pygame
from game_object import GameObject
from collections import defaultdict
from asset_factory import load_player_animations, get_background

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


def update(game_state, inputs):
    pressed_buttons = game_state["buttons_held"]
    for key_input in inputs[pygame.KEYDOWN]:
        if key_input.key in [pygame.K_w, pygame.K_a, pygame.K_d]:
            pressed_buttons.append(key_input.key)

    for key_input in inputs[pygame.KEYUP]:
        if key_input.key in pressed_buttons:
            pressed_buttons.remove(key_input.key)

    player = game_state["player"]
    # This needs to be a lot more nuanced
    in_air = player.y < game_state['player_boundaries'][0].bottom - 65
    flying = pygame.K_w in pressed_buttons or (
            in_air and (
                pygame.K_a in pressed_buttons or pygame.K_d in pressed_buttons))
    current_player_animation = "neutral"
    if pygame.K_w in pressed_buttons:
        player.y_vel = max(player.y_vel - 0.45, -2.5)
    if flying:
        if pygame.K_a in pressed_buttons:
            current_player_animation = "fly_left"
            player.x_vel -= 0.025
        elif pygame.K_d in pressed_buttons:
            current_player_animation = "fly_right"
            player.x_vel += 0.025
        else:
            current_player_animation = "fly_neutral"
        if player.x_vel > 0:
            player.x_vel -= player.x_vel // 15
        else:
            player.x_vel += abs(player.x_vel) // 15
    else:
        if not in_air:
            if pygame.K_a in pressed_buttons:
                player.x_vel = -1
            elif pygame.K_d in pressed_buttons:
                player.x_vel = 1
            else:
                player.x_vel = 0

    player.update_animation(current_player_animation)
    player.y_vel = min(player.y_vel + 0.035, 3.5)

    new_x, new_y = player.x + player.x_vel, player.y + player.y_vel
    bound = game_state["player_boundaries"][0]
    if bound.contains(pygame.Rect(new_x, player.y, 64, 64)):
        player.x = new_x
    else:
        player.x_vel = 0

    if bound.contains(pygame.Rect(player.x, new_y, 64, 64)):
        player.y = new_y
    else:
        player.y_vel = 0


def get_screen_coordinate(screen_center, camera_center, point):
    offset_x, offset_y = screen_center.x - camera_center.x, screen_center.y - camera_center.y
    return point.x + offset_x, point.y + offset_y


def draw(screen, game_state):
    player = game_state["player"]
    screen_center = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    camera_center = pygame.math.Vector2(player.x, player.y - 80)

    def calc_screen_position(point):
        return get_screen_coordinate(screen_center, camera_center, point)

    screen.fill((123, 123, 123))
    for bg_image, bg_top_left in game_state["backgrounds"]:
        screen.blit(bg_image, calc_screen_position(bg_top_left))

    screen.blit(player.get_sprite(), calc_screen_position(pygame.Vector2(player.x, player.y)))
    bound = game_state['player_boundaries'][0]
    corners = [(bound.left, bound.top), (bound.right, bound.top), (bound.right, bound.bottom), (bound.left, bound.bottom)]
    point_list = [calc_screen_position(pygame.Vector2(corner)) for corner in corners]
    pygame.draw.polygon(screen, (255, 0, 0), point_list, 2)
    pygame.display.update()


def main():
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Valkyrie")

    input_event_types = [pygame.KEYDOWN,
                         pygame.KEYUP,
                         pygame.MOUSEBUTTONUP,
                         pygame.MOUSEBUTTONDOWN,
                         pygame.MOUSEMOTION]
    bg_sprite = get_background()
    game_state = {
        "player": GameObject(initial_pos=(1, 1),
                             initial_vel=(0, 0),
                             animations=load_player_animations()),
        "backgrounds": [(bg_sprite, pygame.Vector2(-350, -300))],
        "buttons_held": [],
        "player_boundaries": [pygame.Rect(0, 0, 1200, 900)]
    }

    running = True
    while running:
        inputs = defaultdict(list)
        for event in pygame.event.get():
            if event.type in input_event_types:
                inputs[event.type].append(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

        update(game_state, inputs)
        draw(window, game_state)
    pygame.quit()


if __name__ == "__main__":
    main()
