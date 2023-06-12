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

    vertex = [(vertex[0]),
              (vertex[1] * cos - vertex[2] * sin),
              (vertex[1] * sin + vertex[2] * cos)]

    return vertex


def vertex_rotate_y(vertex, angle):
    cos = math.cos(angle)
    sin = math.sin(angle)

    # rotation_matrix = [[cos, 0, sin, 0], [0, 1, 0, 0], [-sin, 0, cos, 0], [0, 0, 0, 1]]

    vertex = [(vertex[0] * cos + vertex[2] * sin),
              (vertex[1]),
              (-(vertex[0] * sin) + vertex[2] * cos)]

    return vertex


def vertex_rotate_z(vertex, angle):
    cos = math.cos(angle)
    sin = math.sin(angle)

    # rotation_matrix = [[cos, -sin, 0, 0], [sin, cos, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    vertex = [(vertex[0] * cos - vertex[1] * sin),
              (vertex[0] * sin + vertex[1] * cos),
              (vertex[2])]

    return vertex


def vertex_translate(vertex, offset):
    vertex = (vertex[0] + offset[0], vertex[1] + offset[1], vertex[2] + offset[2])
    return vertex
