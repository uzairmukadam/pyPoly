import math


def vector_angle(v1, v2, c):
    v1 = v1[0] - c[0], v1[1] - c[1], v1[2] - c[2]
    v2 = v2[0] - c[0], v2[1] - c[1], v2[2] - c[2]

    nume = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
    deno = vector_length(v1) * vector_length(v2)

    res = nume / deno

    return res


def light_vector_angle(v1, v2, c):
    v1 = v1[0] - c[0], v1[1] - c[1], v1[2] - c[2]

    nume = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
    deno = vector_length(v1) * vector_length(v2)

    res = nume / deno

    return res


def vector_length(v):
    return math.sqrt((v[0] ** 2) + (v[1] ** 2) + (v[2] ** 2)) + 0.0001


def vertex_rotate_x(vertex, angle):
    cos = math.cos(angle)
    sin = math.sin(angle)

    # rotation_matrix = [[1, 0, 0, 0], [0, cos, -sin, 0], [0, sin, cos, 0], [0, 0, 0, 1]]

    res = [(vertex[0]),
           (vertex[1] * cos - vertex[2] * sin),
           (vertex[1] * sin + vertex[2] * cos)]

    return res


def vertex_rotate_y(vertex, angle):
    cos = math.cos(angle)
    sin = math.sin(angle)

    # rotation_matrix = [[cos, 0, sin, 0], [0, 1, 0, 0], [-sin, 0, cos, 0], [0, 0, 0, 1]]

    res = [(vertex[0] * cos + vertex[2] * sin),
           (vertex[1]),
           (-(vertex[0] * sin) + vertex[2] * cos)]

    return res


def vertex_rotate_z(vertex, angle):
    cos = math.cos(angle)
    sin = math.sin(angle)

    # rotation_matrix = [[cos, -sin, 0, 0], [sin, cos, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    res = [(vertex[0] * cos - vertex[1] * sin),
           (vertex[0] * sin + vertex[1] * cos),
           (vertex[2])]

    return res


def vertex_translate(vertex, offset):
    res = (vertex[0] + offset[0], vertex[1] + offset[1], vertex[2] + offset[2])
    return res


def normal_calculation(pts, center):
    v1 = [pts[1][0] - pts[0][0], pts[1][1] - pts[0][1], pts[1][2] - pts[0][2]]
    v2 = [pts[2][0] - pts[0][0], pts[2][1] - pts[0][1], pts[2][2] - pts[0][2]]

    res = [(v1[1] * v2[2] - v1[2] * v2[1]),
           (v1[2] * v2[0] - v1[0] * v2[2]),
           (v1[0] * v2[1] - v1[1] * v2[0])]

    length = vector_length(res)
    res[0] /= length
    res[1] /= length
    res[2] /= length

    return vertex_translate(res, center)


class SceneManagement:
    def __init__(self, engine):
        self.engine = engine

        self.light_vector = (0, 0, -1)

        self.vertices = []
        self.faces = []

        self.normal = []

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
        camera_rot = self.engine.camera.angle_x, self.engine.camera.angle_y, self.engine.camera.angle_z

        view_offset = -camera_pos[0], camera_pos[1], -camera_pos[2]

        self.vertices = []
        self.faces = []

        obj = self.engine.model.obj

        for face in obj['f']:
            vertices = (obj['v'][face[0]], obj['v'][face[1]], obj['v'][face[2]])
            center = ((vertices[0][0] + vertices[1][0] + vertices[2][0]) / 3,
                      (vertices[0][1] + vertices[1][1] + vertices[2][1]) / 3,
                      (vertices[0][2] + vertices[1][2] + vertices[2][2]) / 3)
            normal = normal_calculation(vertices, center)

            ##

            # get light data

            if camera_rot[0] != 0:
                center = vertex_rotate_x(center, camera_rot[0])
                normal = vertex_rotate_x(normal, camera_rot[0])

            if camera_rot[1] != 0:
                center = vertex_rotate_y(center, camera_rot[1])
                normal = vertex_rotate_y(normal, camera_rot[1])

            if camera_rot[2] != 0:
                center = vertex_rotate_z(center, camera_rot[2])
                normal = vertex_rotate_z(normal, camera_rot[2])

            light_vector = self.projection_vertex(self.light_vector)
            light_angle = light_vector_angle(vertex_translate(normal, view_offset), self.light_vector,
                                             vertex_translate(center, view_offset))
            camera_angle = math.acos(
                vector_angle(vertex_translate(normal, view_offset), (0, 0, 0),
                             vertex_translate(center, view_offset)))

            center = self.projection_vertex(vertex_translate(center, view_offset))
            normal = self.projection_vertex(vertex_translate(normal, view_offset))

            # translate normal and check with camera vector
            is_visible = math.pi / 2 >= camera_angle >= 0

            if is_visible:
                triangle = []
                for i in range(3):
                    vertex = vertices[i]

                    if camera_rot[0] != 0:
                        vertex = vertex_rotate_x(vertex, camera_rot[0])

                    if camera_rot[1] != 0:
                        vertex = vertex_rotate_y(vertex, camera_rot[1])

                    if camera_rot[2] != 0:
                        vertex = vertex_rotate_z(vertex, camera_rot[2])

                    vertex = vertex_translate(vertex, view_offset)

                    vertex = self.projection_vertex(vertex)

                    if vertex not in self.vertices:
                        self.vertices.append(vertex)

                    triangle.append(self.vertices.index(vertex))

                self.faces.append(
                    {'f': tuple(triangle), 'c': center, 'n': normal, 'lv': light_vector, 'li': light_angle})
