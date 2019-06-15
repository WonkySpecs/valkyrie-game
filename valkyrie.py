import pygame
from game_object import GameObject
from collections import defaultdict
from asset_factory import get_sprite, Entity

WIDTH = 640
HEIGHT = 480

input_event_types = [pygame.KEYDOWN,
                     pygame.KEYUP,
                     pygame.MOUSEBUTTONUP,
                     pygame.MOUSEBUTTONDOWN,
                     pygame.MOUSEMOTION]

bg = get_sprite(Entity.BACKGROUND)

pressed_buttons = []


def update(game_state, inputs):
    player = game_state["player"]
    for key_input in inputs[pygame.KEYDOWN]:
        if key_input.key in [pygame.K_w, pygame.K_a, pygame.K_d]:
            pressed_buttons.append(key_input.key)

    for key_input in inputs[pygame.KEYUP]:
        if key_input.key in pressed_buttons:
            pressed_buttons.remove(key_input.key)

    if pygame.K_w in pressed_buttons:
        player.y_vel = max(player.y_vel - 0.55, -2.2)

    x_vel = 0
    if pygame.K_a in pressed_buttons:
        x_vel -= 1
    if pygame.K_d in pressed_buttons:
        x_vel += 1
    player.x_vel = x_vel
    player.y_vel = min(player.y_vel + 0.03, 3.5)
    if player.y_vel > 0 and player.y > HEIGHT - 80:
        player.y_vel = 0
    player.x += player.x_vel
    player.y += player.y_vel


def draw(window, game_state):
    window.fill((123, 123, 123))
    window.blit(bg, (0, 0))
    player = game_state["player"]
    window.blit(player.get_sprite(), (player.x, player.y))
    pygame.display.update()


def main():
    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Valkyrie")

    game_state = {
        "player": GameObject(initial_pos=(WIDTH // 2, HEIGHT // 2),
                             initial_vel=(0, 0),
                             sprites={"neutral": [get_sprite(Entity.PLAYER)]})
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
