import pygame
from OpenGL.GL import *
from ui import init_ui, render_ui, cleanup_ui, update_fps
from renderer import render_scene, init_opengl
from adt_loader import ADTLoader

# Screen settings
WIDTH, HEIGHT = 1280, 720

# Global state
adt_data = None
rotation_x, rotation_y = 0, 0
camera_distance = 150
camera_position = [0, 50, 150]  # [x, y, z]
mouse_sensitivity = 0.2
is_mouse_dragging = False
last_mouse_pos = (0, 0)

def load_adt_callback(file_path):
    """Callback to load ADT file."""
    global adt_data
    print(f"Loading ADT file: {file_path}")
    adt_loader = ADTLoader()
    adt_data = adt_loader.load_adt(file_path)

def handle_input():
    """Handle camera and input controls."""
    global rotation_x, rotation_y, camera_distance, camera_position
    keys = pygame.key.get_pressed()

    # WASD for panning
    speed = 2
    if keys[pygame.K_w]:  # Forward
        camera_position[2] -= speed
    if keys[pygame.K_s]:  # Backward
        camera_position[2] += speed
    if keys[pygame.K_a]:  # Left
        camera_position[0] -= speed
    if keys[pygame.K_d]:  # Right
        camera_position[0] += speed

    # Handle zooming
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Mouse wheel up
                camera_distance = max(camera_distance - 5, 50)
            elif event.button == 5:  # Mouse wheel down
                camera_distance = min(camera_distance + 5, 300)

def handle_mouse_events():
    """Handle mouse input for rotation."""
    global rotation_x, rotation_y, is_mouse_dragging, last_mouse_pos

    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  # Left mouse button held
        if not is_mouse_dragging:
            is_mouse_dragging = True
            last_mouse_pos = pygame.mouse.get_pos()
        else:
            current_mouse_pos = pygame.mouse.get_pos()
            delta_x = current_mouse_pos[0] - last_mouse_pos[0]
            delta_y = current_mouse_pos[1] - last_mouse_pos[1]
            rotation_x += delta_y * mouse_sensitivity
            rotation_y += delta_x * mouse_sensitivity
            last_mouse_pos = current_mouse_pos
    else:
        is_mouse_dragging = False

def main():
    global adt_data, rotation_x, rotation_y, camera_distance

    # Initialize Pygame and OpenGL
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("ADT Viewer")
    init_opengl(WIDTH, HEIGHT)

    # Set the background color
    glClearColor(0.8, 0.8, 0.8, 1.0)

    # Initialize the UI
    init_ui(load_adt_callback)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle input
        handle_input()
        handle_mouse_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Render the scene if adt_data is available
        if adt_data:
            render_scene(adt_data, rotation_x, rotation_y, camera_distance, camera_position)

        # Update FPS and pass it to the UI
        fps = clock.get_fps()
        update_fps(fps)

        # Render the UI
        render_ui()

        pygame.display.flip()
        clock.tick(60)  # Cap FPS at 60

    cleanup_ui()
    pygame.quit()

if __name__ == "__main__":
    main()
