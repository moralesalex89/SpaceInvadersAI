class Settings:

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (35, 35, 35)

        self.ship_speed_factor = 5
        self.ship_limit = 0

        self.bullet_speed_factor = 10
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        self.bullet_delay = 5

        self.alien_points_a = 40
        self.alien_points_b = 20
        self.alien_points_c = 10
        self.alien_points_ufo = 200
        self.alien_bullet_speed_factor = 5
        self.alien_space_factor = 25
        self.alien_fleet_cols = 11
        self.alien_fleet_rows = 5
        self.alien_width = 60
        self.alien_height = 40
        self.alien_frame_factor = 60
        self.alien_speed_factor = 0.5
        self.fleet_drop_speed = self.alien_space_factor + self.alien_height
        self.fleet_direction = 1
        self.ufo_speed_factor = 1
        self.alien_start_pos_x = (self.screen_width - (self.alien_width * self.alien_fleet_cols)
                                  - (self.alien_space_factor * self.alien_fleet_cols)) / 2
        self.alien_start_pos_y = 95

        self.barrier_topy = 650
        self.barrier_height = 40
        self.barrier_width = 35
        self.barrier_total = 3
        self.barrier_count_x = 3
        self.barrier_count_y = 2

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 5
        self.ufo_speed_factor = 1
        self.bullet_speed_factor = 10
        self.alien_speed_factor = 0.5
        self.alien_frame_factor = 60
        self.fleet_direction = 1
        self.alien_points_a = 40
        self.alien_points_b = 20
        self.alien_points_c = 10
        self.alien_points_ufo = 200

    def increase_speed(self):
        self.alien_frame_factor /= self.speedup_scale
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.ufo_speed_factor *= self.speedup_scale
        self.alien_points_a = int(self.alien_points_a * self.score_scale)
        self.alien_points_b = int(self.alien_points_b * self.score_scale)
        self.alien_points_c = int(self.alien_points_c * self.score_scale)
        self.alien_points_ufo = int(self.alien_points_ufo * self.score_scale)
