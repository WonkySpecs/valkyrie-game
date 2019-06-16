import pygame
from game_object import GameObject
from collections import defaultdict
from asset_factory import load_player_animations, get_background
from typing import List, Tuple

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


def rect_tuple_to_sides(rect):
    # A replacement for pygame Rects, as they use inverted y axis: may regret later
    left = rect[0]
    right = rect[0] + rect[2]
    top = rect[1]
    bottom = rect[1] - rect[3]
    return left, right, top, bottom


def inside_boundaries(boundaries: List[Tuple], player_rect: Tuple) -> bool:
    player_left, player_right, player_top, player_bottom = rect_tuple_to_sides(player_rect)
    for boundary_rect in boundaries:
        left, right, top, bottom = rect_tuple_to_sides(boundary_rect)
        if player_left >= left and player_right <= right and player_top <= top and player_bottom >= bottom:
            return True

    return False


def update(game_state, inputs, level):
    pressed_buttons = game_state["buttons_held"]
    for key_input in inputs[pygame.KEYDOWN]:
        if key_input.key in [pygame.K_w, pygame.K_a, pygame.K_d]:
            pressed_buttons.append(key_input.key)

    for key_input in inputs[pygame.KEYUP]:
        if key_input.key in pressed_buttons:
            pressed_buttons.remove(key_input.key)

    player = game_state["player"]
    # This needs to be a lot more nuanced
    in_air = player.y > 0
    flying = pygame.K_w in pressed_buttons or (
                in_air and (
                    pygame.K_a in pressed_buttons or pygame.K_d in pressed_buttons))
    current_player_animation = "neutral"
    if pygame.K_w in pressed_buttons:
        player.y_vel = min(player.y_vel + 0.45, 2.5)
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
    player.y_vel = max(player.y_vel - 0.035, -3.5)

    new_x, new_y = player.x + player.x_vel, player.y + player.y_vel
    if inside_boundaries(level["player_boundaries"], pygame.Rect(new_x, player.y, 64, 64)):
        player.x += player.x_vel
    else:
        player.x_vel = 0

    if inside_boundaries(level["player_boundaries"], pygame.Rect(player.y, new_y, 64, 64)):
        player.y += player.y_vel
    else:
        player.y_vel = 0


def get_screen_coordinate(screen_center, world_camera_center, world_top_left):
    offset = world_top_left - world_camera_center
    return screen_center.x + offset.x, screen_center.y - offset.y


def draw(screen, game_state):
    player = game_state["player"]
    world_camera_center = pygame.math.Vector2(player.x, player.y + 80)
    screen_center = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def calc_screen_position(top_left):
        return get_screen_coordinate(screen_center, world_camera_center, top_left)

    screen.fill((123, 123, 123))
    for bg_image, bg_top_left in game_state["backgrounds"]:
        screen.blit(bg_image, calc_screen_position(bg_top_left))

    screen.blit(player.get_sprite(), calc_screen_position(pygame.Vector2(player.x, player.y)))
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
        "player": GameObject(initial_pos=(0, 0),
                             initial_vel=(0, 0),
                             animations=load_player_animations()),
        "backgrounds": [(bg_sprite, pygame.Vector2(-350, 950))],
        "buttons_held": []
    }

    level = {
        "player_boundaries": [(-350, 950, 1600, 1200)]
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

        update(game_state, inputs, level)
        draw(window, game_state)
    pygame.quit()


if __name__ == "__main__":
    main()
