import sys

from camera import *
from object import *
from scene_management import *
from settings import *
from wireframe_renderer import *


def check_event():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()


class Main:
    def __init__(self):
        # initiate pygame and settings
        pg.init()
        self.settings = Settings()

        # setting up pygame window
        self.screen = pg.display.set_mode(self.settings.resolution, self.settings.window_mode)
        self.clock = pg.time.Clock()
        self.delta_time = self.clock.tick(self.settings.fps)

        # initialize classes
        self.model = Model()  # stores the vertices and faces of the model
        self.camera = Camera(self)  # deals with the movement of the camera
        self.scene_management = SceneManagement(self)  # transformation of the model based on camera position
        self.renderer = WireframeRenderer(self)  # draws the model with wireframe mode

    def update(self):
        pg.display.flip()

        self.delta_time = self.clock.tick(self.settings.fps)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

        self.camera.update()
        self.scene_management.update()
        self.renderer.update()

    def draw(self):
        self.screen.fill((40, 60, 80))

        self.renderer.draw()

    def run(self):
        while True:
            check_event()
            self.update()
            self.draw()


if __name__ == "__main__":
    main = Main()
    main.run()
