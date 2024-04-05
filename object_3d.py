from math import sqrt

import pygame as pg
from numba import njit

from matrix_functions import *


@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


class Object3D:
    def __init__(self, render, vertices='', faces=''):
        self.render = render
        self.vertices = np.array([np.array(v) for v in vertices])
        self.faces = np.array([np.array(face) for face in faces])
        self.translate([0.0001, 0.0001, 0.0001])

        self.font = pg.font.SysFont('Arial', 30, bold=True)
        self.color_faces = [(pg.Color('#FEE715FF'), face) for face in self.faces]
        self.movement_flag, self.draw_vertices = False, False

    def draw(self):
        self.screen_projection()
        self.movement()

    def movement(self):
        if self.movement_flag:
            self.rotate_y(-(pg.time.get_ticks() % 0.005))

    def screen_projection(self):
        vertices = self.vertices @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projection_matrix
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices_2d = vertices[:, :2]

        for color_face in self.color_faces:
            color, face = color_face
            polygon_2d = vertices_2d[face]
            polygon = vertices[face]
            # getting normal
            line1 = [
                polygon[1][0] - polygon[0][0],
                polygon[1][1] - polygon[0][1],
                polygon[1][2] - polygon[0][2],
            ]
            line2 = [
                polygon[2][0] - polygon[0][0],
                polygon[2][1] - polygon[0][1],
                polygon[2][2] - polygon[0][2],
            ]
            normal = [
                line1[1] * line2[2] - line1[2] * line2[1],
                line1[2] * line2[0] - line1[0] * line2[2],
                line1[0] * line2[1] - line1[1] * line2[0],
            ]
            l = sqrt(normal[0]*normal[0] + normal[1]*normal[1] + normal[2]*normal[2])
            normal[0] /= l
            normal[1] /= l
            normal[2] /= l
            # /getting normal
            if normal[2] > 0 and not any_func(
                    polygon_2d, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.polygon(self.render.screen, color, polygon_2d, 1)

        if self.draw_vertices:
            for vertex in vertices_2d:
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)

    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    def scale(self, scale_to):
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)


class Axes(Object3D):
    def __init__(self, render):
        super().__init__(render)
        self.vertices = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = False
        self.label = 'XYZ'
