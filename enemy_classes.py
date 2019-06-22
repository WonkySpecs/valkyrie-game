from game_objects import GameObject
import asset_factory
import pygame


class AssaultSoldier(GameObject):
    def __init__(self,
                 initial_pos=None,
                 initial_vel=(0, 0),
                 move_speed=5):
        super().__init__(hitbox=pygame.Rect(initial_pos[0], initial_pos[1], 24, 50),
                         initial_vel=initial_vel,
                         move_speed=move_speed,
                         animations=asset_factory.assault_soldier_green(),
                         initial_animation='neutral',
                         image_offset=(-12, -9))

    def update_velocity(self, dt):
        self.y_vel = self.y_vel + dt * GameObject.gravity
        self.y_vel -= self.drag * self.y_vel * dt
