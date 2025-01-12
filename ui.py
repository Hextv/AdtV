from dearpygui.dearpygui import *
import os

# Global variables
selected_file_path = None
file_load_callback = None
current_directory = os.getcwd()
file_buttons = []  # Keep track of dynamically added file buttons
grid_enabled = True
lighting_enabled = True

def init_ui(load_adt_callback):
    """Initialize the upgraded DearPyGui interface."""
    global file_load_callback
    file_load_callback = load_adt_callback

    create_context()
    create_viewport(title="ADT Viewer UI", width=800, height=600)

    with window(label="ADT Viewer", width=800, height=600):
        with tab_bar():
            # File Browser Tab
            with tab(label="File Browser"):
                add_text("Browse for ADT Files:")
                add_button(label="Open File Browser", callback=show_file_browser)
                add_text("", tag="selected_file_text")
                add_button(label="Load Selected File", callback=load_selected_file)
                add_separator()
                with child_window(tag="file_browser_window", width=780, height=400):
                    add_text("File Browser Contents", tag="file_browser_header")
                    add_separator()

            # Camera Settings Tab
            with tab(label="Camera Settings"):
                add_text("Adjust Camera Position:")
                add_slider_float(label="X Position", default_value=0, min_value=-200, max_value=200, callback=update_camera_position, user_data=0)
                add_slider_float(label="Y Position", default_value=50, min_value=-200, max_value=200, callback=update_camera_position, user_data=1)
                add_slider_float(label="Zoom", default_value=150, min_value=50, max_value=300, callback=update_camera_distance)

            # Rendering Options Tab
            with tab(label="Rendering Options"):
                add_text("Rendering Settings:")
                add_checkbox(label="Enable Grid", default_value=True, callback=toggle_grid)
                add_checkbox(label="Enable Lighting", default_value=True, callback=toggle_lighting)
                add_color_edit(label="Background Color", default_value=[0.8, 0.8, 0.8, 1.0], callback=update_background_color)

            # Performance Stats Tab
            with tab(label="Performance Stats"):
                add_text("Rendering Stats:")
                add_text("FPS: ", tag="fps_text")
                add_text("Triangles Rendered: ", tag="triangles_text")

    setup_dearpygui()
    show_viewport()

def render_ui():
    """Render the DearPyGui interface."""
    while is_dearpygui_running():
        render_dearpygui_frame()

def cleanup_ui():
    """Clean up DearPyGui resources."""
    destroy_context()

def update_fps(fps):
    """Update the FPS display in the UI."""
    set_value("fps_text", f"FPS: {fps:.2f}")

# File Browser Functions
def show_file_browser(sender, app_data, user_data):
    """Display the file browser."""
    populate_file_browser(current_directory)

def populate_file_browser(directory):
    """Populate the file browser with files and folders dynamically."""
    global file_buttons

    # Update header to show the current directory
    configure_item("file_browser_header", label=f"Current Directory: {directory}")

    # Remove existing file buttons by hiding them
    for button in file_buttons:
        hide_item(button)

    # Add "Go Up" button for parent directory navigation
    parent_dir = os.path.dirname(directory)
    go_up_button = f"go_up_button_{directory}"
    if parent_dir != directory and not does_item_exist(go_up_button):
        add_button(label=".. (Go Up)", tag=go_up_button, parent="file_browser_window",
                   callback=navigate_to_directory, user_data=parent_dir)
        file_buttons.append(go_up_button)

    # Add buttons for files and folders
    for entry in sorted(os.listdir(directory)):
        full_path = os.path.join(directory, entry)
        button_tag = f"file_button_{entry}"
        if os.path.isdir(full_path):
            if not does_item_exist(button_tag):
                add_button(label=f"[DIR] {entry}", tag=button_tag, parent="file_browser_window",
                           callback=navigate_to_directory, user_data=full_path)
                file_buttons.append(button_tag)
            else:
                show_item(button_tag)
        elif entry.endswith(".adt"):
            if not does_item_exist(button_tag):
                add_button(label=entry, tag=button_tag, parent="file_browser_window",
                           callback=select_file, user_data=full_path)
                file_buttons.append(button_tag)
            else:
                show_item(button_tag)

def navigate_to_directory(sender, app_data, user_data):
    """Navigate to a different directory."""
    global current_directory
    current_directory = user_data
    populate_file_browser(current_directory)

def select_file(sender, app_data, user_data):
    """Select a file from the browser."""
    global selected_file_path
    selected_file_path = user_data
    set_value("selected_file_text", f"Selected File: {os.path.basename(selected_file_path)}")

def load_selected_file(sender, app_data, user_data):
    """Load the selected file dynamically."""
    global selected_file_path
    if selected_file_path and os.path.isfile(selected_file_path):
        print(f"Loading file: {selected_file_path}")
        if file_load_callback:
            file_load_callback(selected_file_path)  # Directly trigger the callback
    else:
        print("No valid file selected.")

# Camera and Rendering Functions
def update_camera_position(sender, app_data, user_data):
    """Update camera position dynamically."""
    from main import camera_position  # Import the camera position from main
    camera_position[user_data] = app_data

def update_camera_distance(sender, app_data, user_data):
    """Update camera zoom dynamically."""
    from main import camera_distance  # Import the camera distance from main
    camera_distance = app_data

def toggle_grid(sender, app_data, user_data):
    """Toggle grid rendering."""
    global grid_enabled
    grid_enabled = app_data

def toggle_lighting(sender, app_data, user_data):
    """Toggle lighting."""
    global lighting_enabled
    lighting_enabled = app_data
    if lighting_enabled:
        glEnable(GL_LIGHTING)
    else:
        glDisable(GL_LIGHTING)

def update_background_color(sender, app_data, user_data):
    """Update background color."""
    glClearColor(app_data[0], app_data[1], app_data[2], app_data[3])
