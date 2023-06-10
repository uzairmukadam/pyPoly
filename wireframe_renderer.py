import pygame as pg


class WireframeRenderer:
    def __init__(self, engine):
        self.engine = engine
        self.screen = engine.screen

        self.vertices = []
        self.faces = []

    def update(self):
        self.vertices = self.engine.scene_management.vertices
        self.faces = self.engine.scene_management.faces

    def draw(self):
        for face in self.faces:
            pts = face['f']
            center = face['c'][:-1]
            normal = face['n'][:-1]

            p1 = self.vertices[pts[0]]
            p2 = self.vertices[pts[1]]
            p3 = self.vertices[pts[2]]

            pg.draw.polygon(self.screen, "white",
                            ((p1[0], p1[1]), (p2[0], p2[1]), (p3[0], p3[1])), 1)

            # normal
            # pg.draw.line(self.screen, "blue", center, normal, 1)
