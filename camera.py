import math

import pygame as pg


class Camera:
    def __init__(self, engine):
        self.engine = engine

        self.pos_x, self.pos_y, self.pos_z = 0, 0, 0
        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0

    def update(self):
        dx, dy, dz = 0, 0, 0
        ax, ay, az = 0, 0, 0

        keys = pg.key.get_pressed()

        movement_speed = (1 / 100) * self.engine.delta_time
        rotation_speed = (math.pi / 1000) * self.engine.delta_time

        if keys[pg.K_w]:
            dz += movement_speed
        if keys[pg.K_s]:
            dz -= movement_speed

        if keys[pg.K_a]:
            dx -= movement_speed
        if keys[pg.K_d]:
            dx += movement_speed

        if keys[pg.K_q]:
            dy -= movement_speed
        if keys[pg.K_e]:
            dy += movement_speed

        self.pos_x += dx
        self.pos_y += dy
        self.pos_z += dz

        # set vertical angle change limit

        if keys[pg.K_UP]:
            ax += rotation_speed
        if keys[pg.K_DOWN]:
            ax -= rotation_speed

        if keys[pg.K_LEFT]:
            ay += rotation_speed
        if keys[pg.K_RIGHT]:
            ay -= rotation_speed

        if keys[pg.K_z]:
            az += rotation_speed
        if keys[pg.K_x]:
            az -= rotation_speed

        self.angle_x += ax
        self.angle_y += ay
        self.angle_z += az

        if keys[pg.K_r]:
            self.angle_x = 0
            self.angle_y = 0
            self.angle_z = 0
