import math


# using shoelace method
def basic_back_face_culling(p1, p2, p3):
    val = ((p1[0] * p2[1]) - (p1[1] * p2[0])) + ((p2[0] * p3[1]) - (p2[1] * p3[0])) + (
            (p3[0] * p1[1]) - (p3[1] * p1[0]))

    return val >= 0


def vector_length(v):
    return math.sqrt((v[0] ** 2) + (v[1] ** 2) + (v[2] ** 2)) + 0.0001


def vertex_rotate_x(vertex, angle):
    cos = math.cos(angle)
    sin = math.sin(angle)

    # rotation_matrix = [[1, 0, 0, 0], [0, cos, -sin, 0], [0, sin, cos, 0], [0, 0, 0, 1]]

    res = [(vertex[0]),
           (vertex[1] * cos - vertex[2] * sin),
           (vertex[1] * sin + vertex[2] * cos),
           1]

    return res


def vertex_rotate_y(vertex, angle):
    cos = math.cos(angle)
    sin = math.sin(angle)

    # rotation_matrix = [[cos, 0, sin, 0], [0, 1, 0, 0], [-sin, 0, cos, 0], [0, 0, 0, 1]]

    res = [(vertex[0] * cos + vertex[2] * sin),
           (vertex[1]),
           (-(vertex[0] * sin) + vertex[2] * cos),
           1]

    return res


def vertex_rotate_z(vertex, angle):
    cos = math.cos(angle)
    sin = math.sin(angle)

    # rotation_matrix = [[cos, -sin, 0, 0], [sin, cos, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    res = [(vertex[0] * cos - vertex[1] * sin),
           (vertex[0] * sin + vertex[1] * cos),
           (vertex[2]),
           1]

    return res


def vertex_translate(vertex, offset):
    res = (vertex[0] + offset[0], vertex[1] + offset[1], vertex[2] + offset[2], 1)
    return res


def normal_calculation(pts, center):
    v1 = [pts[1][0] - pts[0][0], pts[1][1] - pts[0][1], pts[1][2] - pts[0][2]]
    v2 = [pts[2][0] - pts[0][0], pts[2][1] - pts[0][1], pts[2][2] - pts[0][2]]

    res = [(v1[1] * v2[2] - v1[2] * v2[1]),
           (v1[2] * v2[0] - v1[0] * v2[2]),
           (v1[0] * v2[1] - v1[1] * v2[0]),
           1]

    length = vector_length(res)
    res[0] /= length
    res[1] /= length
    res[2] /= length

    return vertex_translate(res, center)


class SceneManagement:
    def __init__(self, engine):
        self.engine = engine

        self.vertices = []
        self.faces = []

        self.normal = []

    def projection_vertex(self, vertex):
        width = self.engine.settings.width
        height = self.engine.settings.height
        screen_distance = self.engine.settings.screen_distance

        projection_factor = screen_distance / (vertex[2] + 0.0001)

        temp = [vertex[0] * projection_factor, vertex[1] * projection_factor, 1]

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
            pts = obj['v'][face[0]], obj['v'][face[1]], obj['v'][face[2]]
            center = (pts[0][0] + pts[1][0] + pts[2][0]) / 3, (pts[0][1] + pts[1][1] + pts[2][1]) / 3, (
                    pts[0][2] + pts[1][2] + pts[2][2]) / 3
            normal = normal_calculation(pts, center)

            center = vertex_rotate_x(center, camera_rot[0])
            center = vertex_rotate_y(center, camera_rot[1])
            center = vertex_rotate_z(center, camera_rot[2])
            center = vertex_translate(center, view_offset)

            center = self.projection_vertex(center)

            normal = vertex_rotate_x(normal, camera_rot[0])
            normal = vertex_rotate_y(normal, camera_rot[1])
            normal = vertex_rotate_z(normal, camera_rot[2])
            normal = vertex_translate(normal, view_offset)
            normal = self.projection_vertex(normal)

            if True:

                triangle = []
                for i in range(3):
                    pt = pts[i]

                    trans_vert = vertex_rotate_x(pt, camera_rot[0])
                    trans_vert = vertex_rotate_y(trans_vert, camera_rot[1])
                    trans_vert = vertex_rotate_z(trans_vert, camera_rot[2])
                    trans_vert = vertex_translate(trans_vert, view_offset)

                    proj_vert = self.projection_vertex(trans_vert)

                    if proj_vert not in self.vertices:
                        self.vertices.append(proj_vert)
                    triangle.append(self.vertices.index(proj_vert))
                if basic_back_face_culling(self.vertices[triangle[0]], self.vertices[triangle[1]],
                                           self.vertices[triangle[2]]):
                    self.faces.append(
                        {'f': tuple(triangle), 'c': center, 'n': normal})
