
# PyPoly

A 3D software renderer for projecting obj files. The project is created in python using the pygame module

# Controls

- W - Move camera forwards
- S - Move camera backwards
- A - Move camera left
- D - Move camera right
- Up and Down Arrow - Rotate model around its x-axis
- Left and Right Arrow - Rotate model around its y-axis
- Z and X - Rotate model around its z-axis

# Index

1. Working
2. Class files

# Working

All the vertices are stored in a list and the faces are stored in another list. Using transformation matrices, the vertices are moved and rotated based on the button pressed. After transformation these points are passed through the projection matix to project them to 2d plane.

# Class files

1. main.py - This is the starting point of the project and it is responsible for importing all the other required classes and creating the pygame windows for drawing the graphics.
2. settings.py - This class is just used to define parameters to be used by the game engine like window resolution and field of view.
3. object.py - This imports the obj file and segregates the data in it into different variables.
4. camera.py - This class is responsible for dealing with the movement of the camera and the model.
5. scene_management.py - This class is used to calculate the vertex transformation and prjection. It uses the shoelace algorith to implement backface culling. In future normal vectors will be used for backface culling and lighting.
6. wireframe_renderer.py - As the name suggests, this class is responsible for drawing the model in wireframe mode. With the data obtained from the scene_management class it draws the polygons. In future based on polygon normal and light vector, polygon will be colored to depict light shading.
