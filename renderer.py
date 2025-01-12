from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def init_opengl(width, height):
    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)

    # Set up lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_position = [50.0, 100.0, 150.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])

def render_scene(adt_data, rotation_x, rotation_y, camera_distance, camera_position):
    glLoadIdentity()

    # Camera transformation
    gluLookAt(
        camera_position[0], camera_position[1], camera_distance,
        0, 0, 0,
        0, 1, 0
    )

    # Rotate the ADT model
    glPushMatrix()
    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)

    # Render the heightmap
    heightmap = adt_data.get("heightmap", [])
    if heightmap is not None:
        render_heightmap(heightmap)

    glPopMatrix()

    # Render a 3D grid for reference
    render_grid()

def render_heightmap(heightmap):
    grid_size = len(heightmap)
    glBegin(GL_QUADS)
    for x in range(grid_size - 1):
        for z in range(grid_size - 1):
            height = heightmap[x][z]
            glColor3f(height / 20.0, height / 20.0, height / 20.0)
            glVertex3f(x, height, z)
            glVertex3f(x + 1, heightmap[x + 1][z], z)
            glVertex3f(x + 1, heightmap[x + 1][z + 1], z + 1)
            glVertex3f(x, heightmap[x][z + 1], z + 1)
    glEnd()

def render_grid():
    """Render a simple 3D grid for reference."""
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    for i in range(-50, 51, 5):
        glVertex3f(i, 0, -50)
        glVertex3f(i, 0, 50)
        glVertex3f(-50, 0, i)
        glVertex3f(50, 0, i)
    glEnd()
