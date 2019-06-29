import pygame


class Animation:
    def __init__(self, name, frames, durations, offsets=None):
        self.name = name
        self.frames = frames
        self.durations = durations
        self.frame_count = 0
        self.sprite_num = 0
        self.total_duration = sum(durations)
        self.offsets = offsets or [pygame.Vector2(0, 0) for _ in frames]

    def next_frame(self):
        self.frame_count += 1
        if self.frame_count > sum(self.durations[:self.sprite_num + 1]):
            if self.frame_count > self.total_duration:
                self.reset()
            else:
                self.sprite_num += 1

    def get_current_sprite(self):
        return self.frames[self.sprite_num]

    @property
    def image_offset(self):
        return self.offsets[self.sprite_num]

    def reset(self):
        self.frame_count = 0
        self.sprite_num = 0

    def __copy__(self):
        return Animation(self.name,
                         [s.copy() for s in self.frames],
                         self.durations.copy(),
                         self.offsets.copy())
