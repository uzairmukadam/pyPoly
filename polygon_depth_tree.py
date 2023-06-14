class PolygonDepthTree:
    def __init__(self):
        self.root = None

    def add_node(self, parent, face, depth):
        if depth < parent.depth:
            if parent.left is None:
                parent.left = Node(face, depth)
            else:
                self.add_node(parent.left, face, depth)
        else:
            if parent.right is None:
                parent.right = Node(face, depth)
            else:
                self.add_node(parent.right, face, depth)

    def add_polygon(self, face, depth):
        if self.root is None:
            # add data as root Node
            self.root = Node(face, depth)
        else:
            # add data by checking depth
            self.add_node(self.root, face, depth)

    def get_polygons(self):
        pass


class Node:
    def __init__(self, face, depth):
        self.left = None
        self.right = None
        self.face = face
        self.depth = depth
