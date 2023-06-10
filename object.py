import pywavefront


def load_obj(obj_id):
    obj = pywavefront.Wavefront("data/models/" + obj_id + ".obj", collect_faces=True, cache=False)

    return {"v": obj.vertices, "f": obj.mesh_list[0].faces, "p": (0, 0, 0), "r": (0, 0, 0)}


class Model:
    def __init__(self):
        obj_id = "cube"
        self.obj = load_obj(obj_id)
