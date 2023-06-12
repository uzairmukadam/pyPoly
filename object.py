import pywavefront

from transformation import vector_length, vertex_translate


def get_normal(vertices, center):
    v1 = [vertices[1][0] - vertices[0][0], vertices[1][1] - vertices[0][1], vertices[1][2] - vertices[0][2]]
    v2 = [vertices[2][0] - vertices[0][0], vertices[2][1] - vertices[0][1], vertices[2][2] - vertices[0][2]]

    normal = [(v1[1] * v2[2] - v1[2] * v2[1]),
              (v1[2] * v2[0] - v1[0] * v2[2]),
              (v1[0] * v2[1] - v1[1] * v2[0])]

    length = vector_length(normal)

    normal = [vertex / length for vertex in normal]
    return vertex_translate(normal, center)


def load_obj(obj_id):
    obj = pywavefront.Wavefront("data/models/" + obj_id + ".obj", collect_faces=True, cache=False)

    # vertices = [(0, 0, 0), (0, 0, 1), (1, 0, 0)]
    # faces = [(0, 1, 2)]

    vertices = obj.vertices
    faces = obj.mesh_list[0].faces

    centers = []
    normals = []

    for face in faces:
        face_vertices = (vertices[face[0]], vertices[face[1]], vertices[face[2]])

        center = ((face_vertices[0][0] + face_vertices[1][0] + face_vertices[2][0]) / 3,
                  (face_vertices[0][1] + face_vertices[1][1] + face_vertices[2][1]) / 3,
                  (face_vertices[0][2] + face_vertices[1][2] + face_vertices[2][2]) / 3)

        centers.append(center)

        normals.append(get_normal(face_vertices, center))

    print("Object Loaded")

    return {"v": vertices, "f": faces, 'c': centers, 'vn': normals}


class Model:
    def __init__(self):
        obj_id = "teapot"
        self.obj = load_obj(obj_id)
