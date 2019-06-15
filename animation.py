class Animation:
    def __init__(self, name, sprites, durations):
        self.name = name
        self.sprites = sprites
        self.durations = durations
        self.frame_count = 0
        self.sprite_num = 0
        self.total_duration = sum(durations)

    def next_frame(self):
        self.frame_count = (self.frame_count + 1) % self.total_duration
        if self.frame_count > sum(self.durations[:self.sprite_num + 1]):
            self.sprite_num = (self.sprite_num + 1) % len(self.sprites)

    def get_current_sprite(self):
        return self.sprites[self.sprite_num]

    def reset(self):
        self.frame_count = 0
        self.sprite_num = 0
