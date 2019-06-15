import pygame
from game_object import GameObject
from collections import defaultdict
from asset_factory import load_player_animations, get_background

WIDTH = 640
HEIGHT = 480


def update(game_state, inputs):
    pressed_buttons = game_state["buttons_held"]
    for key_input in inputs[pygame.KEYDOWN]:
        if key_input.key in [pygame.K_w, pygame.K_a, pygame.K_d]:
            pressed_buttons.append(key_input.key)

    for key_input in inputs[pygame.KEYUP]:
        if key_input.key in pressed_buttons:
            pressed_buttons.remove(key_input.key)

    player = game_state["player"]
    flying = False
    if pygame.K_w in pressed_buttons:
        player.y_vel = max(player.y_vel - 0.45, -2.5)
        flying = True

    x_vel = 0
    if pygame.K_a in pressed_buttons and player.x > 0:
        x_vel -= 1
    if pygame.K_d in pressed_buttons and player.x < WIDTH - 60:
        x_vel += 1
    current_player_animation = "neutral"
    if flying:
        if player.x_vel == 0:
            current_player_animation = "fly_neutral"
        else:
            current_player_animation = "fly_left" if x_vel < 0 else "fly_right"
    player.update_animation(current_player_animation)
    player.x_vel = x_vel
    player.y_vel = min(player.y_vel + 0.035, 3.5)

    if player.y_vel > 0 and player.y > HEIGHT - 80:
        player.y_vel = 0
    player.x += player.x_vel
    player.y += player.y_vel
    if player.y < 5:
        player.y = 5
        player.y_vel = 0


def draw(window, game_state):
    window.fill((123, 123, 123))
    window.blit(game_state["background"], (0, 0))
    player = game_state["player"]
    window.blit(player.get_sprite(), (player.x, player.y))
    pygame.display.update()


def main():
    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Valkyrie")

    input_event_types = [pygame.KEYDOWN,
                         pygame.KEYUP,
                         pygame.MOUSEBUTTONUP,
                         pygame.MOUSEBUTTONDOWN,
                         pygame.MOUSEMOTION]

    game_state = {
        "player": GameObject(initial_pos=(WIDTH // 2, HEIGHT // 2),
                             initial_vel=(0, 0),
                             animations=load_player_animations()),
        "background": get_background(),
        "buttons_held": []
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
