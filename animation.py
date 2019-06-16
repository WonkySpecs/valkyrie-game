class Animation:
    def __init__(self, name, sprites, durations):
        self.name = name
        self.sprites = sprites
        self.durations = durations
        self.frame_count = 0
        self.sprite_num = 0
        self.total_duration = sum(durations)

    def next_frame(self):
        self.frame_count += 1
        if self.frame_count > sum(self.durations[:self.sprite_num + 1]):
            if self.frame_count > self.total_duration:
                self.reset()
            else:
                self.sprite_num += 1

    def get_current_sprite(self):
        return self.sprites[self.sprite_num]

    def reset(self):
        self.frame_count = 0
        self.sprite_num = 0
