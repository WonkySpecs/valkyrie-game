class GameState:
    def __init__(self,
                 player,
                 clock,
                 enemies=None,
                 player_projectiles=None,
                 enemy_projectiles=None,
                 background_layers=None,
                 terrain=None,
                 hud=None,
                 last_camera_center=None):
        self.player = player
        self.clock = clock
        self.enemies = enemies or []
        self.player_projectiles = player_projectiles or []
        self.enemy_projectiles = enemy_projectiles or []
        self.background_layers = background_layers or {}
        self.terrain = terrain or []
        self.hud = hud or {}
        self.last_camera_center = last_camera_center

    def remove_to_remove_objects(self):
        for l in [self.player_projectiles,
                  self.enemy_projectiles,
                  self.enemies]:
            l[:] = [e for e in l if not e.to_remove]
