import math

from object_3d import Object3D
from camera import Camera
from projection import Projection
import pygame as pg


class SoftwareRender:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.objects = []
        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [10, 0, -30])
        self.projection = Projection(self)
        for i in range(0, 5):
            obj = self.get_object_from_file('resources/sample.obj')
            obj.translate([i * 5, 0, 0])
            self.objects.append(obj)

    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)

    def draw(self):
        self.screen.fill(pg.Color('#101820FF'))
        for obj in self.objects:
            obj.draw()

    def run(self):
        while True:
            self.draw()
            events = pg.event.get()
            keys = pg.key.get_pressed()
            # exiting
            [exit() for i in events if i.type == pg.QUIT]
            if keys[pg.K_ESCAPE]:
                exit()
            # /exiting
            self.camera.control(events, keys)
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)
            pg.mouse.set_visible(0)


if __name__ == '__main__':
    app = SoftwareRender()
    app.run()
