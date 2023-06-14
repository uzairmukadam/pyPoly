import math

import transformation
from polygon_depth_tree import *


def vector_angle(v1, v2, c):
    v1 = v1[0] - c[0], v1[1] - c[1], v1[2] - c[2]
    v2 = v2[0] - c[0], v2[1] - c[1], v2[2] - c[2]

    nume = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
    deno = transformation.vector_length(v1) * transformation.vector_length(v2)

    res = nume / deno

    return res


def light_vector_angle(v1, v2, c):
    v1 = v1[0] - c[0], v1[1] - c[1], v1[2] - c[2]

    nume = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
    deno = transformation.vector_length(v1) * transformation.vector_length(v2)

    res = nume / deno

    return res


class SceneManagement:
    def __init__(self, engine):
        self.engine = engine

        self.light_vector = (0, 0, -1)

        self.vertices = []
        self.faces = None

    def projection_vertex(self, vertex):
        width = self.engine.settings.width
        height = self.engine.settings.height
        screen_distance = self.engine.settings.screen_distance

        projection_factor = screen_distance / (vertex[2] + 0.0001)

        temp = [vertex[0] * projection_factor, vertex[1] * projection_factor]

        temp[0] += width / 2
        temp[1] = (height / 2) - temp[1]

        return tuple(temp)

    def update(self):
        camera_pos = self.engine.camera.pos_x, self.engine.camera.pos_y, self.engine.camera.pos_z
        obj_rot = self.engine.camera.angle_x, self.engine.camera.angle_y, self.engine.camera.angle_z

        view_offset = -camera_pos[0], camera_pos[1] - 0.5, -camera_pos[2] + 5

        self.vertices = []
        self.faces = PolygonDepthTree()

        obj = self.engine.model.obj

        for face in obj['f']:
            face_index = obj['f'].index(face)
            vertices = (obj['v'][face[0]], obj['v'][face[1]], obj['v'][face[2]])
            center = obj['c'][face_index]
            normal = obj['vn'][face_index]

            if obj_rot[0] != 0:
                center = transformation.vertex_rotate_x(center, obj_rot[0])
                normal = transformation.vertex_rotate_x(normal, obj_rot[0])

            if obj_rot[1] != 0:
                center = transformation.vertex_rotate_y(center, obj_rot[1])
                normal = transformation.vertex_rotate_y(normal, obj_rot[1])

            if obj_rot[2] != 0:
                center = transformation.vertex_rotate_z(center, obj_rot[2])
                normal = transformation.vertex_rotate_z(normal, obj_rot[2])

            camera_angle = math.acos(
                vector_angle(transformation.vertex_translate(normal, view_offset), (0, 0, 0),
                             transformation.vertex_translate(center, view_offset)))

            depth = center[2]

            # translate normal and check with camera vector
            is_visible = math.pi / 2 >= camera_angle >= 0

            if is_visible:
                triangle = []
                for i in range(3):
                    vertex = vertices[i]

                    if obj_rot[0] != 0:
                        vertex = transformation.vertex_rotate_x(vertex, obj_rot[0])

                    if obj_rot[1] != 0:
                        vertex = transformation.vertex_rotate_y(vertex, obj_rot[1])

                    if obj_rot[2] != 0:
                        vertex = transformation.vertex_rotate_z(vertex, obj_rot[2])

                    vertex = transformation.vertex_translate(vertex, view_offset)

                    vertex = self.projection_vertex(vertex)

                    if vertex not in self.vertices:
                        self.vertices.append(vertex)

                    triangle.append(self.vertices.index(vertex))

                light_angle = light_vector_angle(transformation.vertex_translate(normal, view_offset),
                                                 self.light_vector,
                                                 transformation.vertex_translate(center, view_offset))

                center = self.projection_vertex(transformation.vertex_translate(center, view_offset))
                normal = self.projection_vertex(transformation.vertex_translate(normal, view_offset))

                data = {'f': tuple(triangle), 'c': center, 'n': normal, 'li': light_angle}

                self.faces.add_polygon(data, depth)
