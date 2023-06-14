import math

import pygame as pg


def get_window_mode(mode=0):
    modes = {
        0: pg.SHOWN,
        1: pg.NOFRAME,
        2: pg.FULLSCREEN
    }

    return modes.get(mode)


class Settings:
    def __init__(self):
        # window parameters
        self.resolution = self.width, self.height = 1280, 720
        self.window_mode = get_window_mode(0)
        self.fps = 0

        # camera parameters
        self.fov = math.pi / 3
        self.screen_distance = (self.width / 2) / (math.tan(self.fov / 2) + 0.0001)
        self.vertical_fov = 2 * (math.atan(self.height / (2 * self.screen_distance)))
        self.z_near = 0.2

        # graphics parameters
        self.draw_distance = 30

        # camera parameters
        self.camera_depth = 10
        self.camera_height = 3

    def load_config(self):
        pass

    def set_config(self):
        pass
