import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps

# import your ui components
from ui.toolbar import Toolbarr
from ui.sidebar import Sidebar
from ui.menu_manager import MenuManager
from ui.properties_panel import PropertiesPanel
from ui.settings_manager import SettingsManager
from layers.layer import Layer
from layers.layer_manager import LayerManager
from ui.layer_panel import LayerPanel

# import you utilities
from utils.keyboard_shortcuts import KeyboardShortcuts

# import your tools
from tools.tools import Toolss

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ModernImageEditor:
    def __init__(self, root):
        self.root = root
        self.settings_manager = SettingsManager(self)
        self.root.title("Modern Image Editor")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        
        
        self.image_path = None
        self.original_image = None
        self.current_image = None
        self.display_image = None
        
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_rect = None
        self.is_cropping = False
        self.active_tool = None
        
        # Initialize undo/redo history
        self.history = []
        self.history_index = -1
        self.max_history = 20  # Maximum number of states to keep in history
        
        self.layer_manager = LayerManager(self)
        self.tools = Toolss(self)
        
        self.settings_manager.apply_settings()
        
        self.create_ui()
        self.keyboard_shortcuts = KeyboardShortcuts(self)  # Add this line
        self.setup_drag_drop()
        self.setup_zoom_functionality()
        self.tools = Toolss(self)
        self.root.bind("<Escape>", self.cancel_text_editing)
        self.menu_manager = MenuManager(self)
        self.menu_manager.settings_manager.apply_settings()
        self.menu_manager.create_menu()
        # Initialize the layer manager
        


    def create_ui(self):
        # Create the toolbar first - it will appear at the top
        self.toolbar = Toolbarr(self)
        self.keyboard_shortcuts = KeyboardShortcuts(self)

        # Create main layout frames
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 10))

        # Create menu bar
        self.menu_manager = MenuManager(self)

        # Left sidebar for tools and adjustments
        self.sidebar = ctk.CTkFrame(self.main_frame, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        # Create the layer panel in the sidebar or a dedicated frame
        self.layer_panel_frame = ctk.CTkFrame(self.sidebar)  # Or another parent frame
        self.layer_panel_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.layer_panel = LayerPanel(self, self.layer_panel_frame)

        # Middle content area for canvas
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right side for properties panel
        self.properties_frame = ctk.CTkFrame(self.main_frame, width=250)
        self.properties_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        # Canvas for image display
        self.canvas_frame = ctk.CTkFrame(self.content_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#2a2d2e", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_frame = ctk.CTkFrame(self.content_frame, height=30)
        self.status_frame.pack(fill=tk.X, pady=(5, 0))

        self.status_bar = ctk.CTkLabel(self.status_frame, text="Ready", anchor="w", padx=10)
        self.status_bar.pack(side=tk.LEFT, fill=tk.X)

        # Resolution label in status bar
        self.resolution_label = ctk.CTkLabel(self.status_frame, text="", padx=10)
        self.resolution_label.pack(side=tk.RIGHT)

        # Zoom level label in status bar
        self.zoom_label = ctk.CTkLabel(self.status_frame, text="Zoom: 100%", padx=10)
        self.zoom_label.pack(side=tk.RIGHT)

        # Create sidebar elements
        self.sidebar_ui = Sidebar(self)

        # Create properties panel on the right side
        self.properties_panel = PropertiesPanel(self, self.properties_frame)

        # Bind canvas events for crop functionality
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
    def activate_draw_tool(self, event=None):
        """Activate the drawing tool."""
        self.active_tool = "draw"
        self.status_bar.configure(text="Draw Tool: Click and drag to draw")
        self.canvas.config(cursor="pencil")  # Change cursor to indicate draw mode
        
        # Show drawing properties in the properties panel
        self.properties_panel.show_draw_properties()
        
        # Set up drawing properties
        if hasattr(self.properties_panel, 'draw_properties'):
            self.draw_color = self.properties_panel.draw_properties["color"]
            self.draw_size = self.properties_panel.draw_properties["size"]
        else:
            self.draw_color = "#FF0000"  # Default red
            self.draw_size = 3  # Default size
        
        self.draw_last_point = None
        
        # Create a temporary image for drawing preview
        if self.current_image:
            from PIL import ImageDraw
            self.draw_overlay = self.current_image.copy()
            self.draw_preview = ImageDraw.Draw(self.draw_overlay)
        
        # Bind canvas events for drawing
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def connect_sidebar_callbacks(self):
        """Connect sidebar UI elements to tool methods after tools are created."""
        self.sidebar_ui.brightness_slider.configure(command=self.tools.apply_brightness)
        self.sidebar_ui.contrast_slider.configure(command=self.tools.apply_contrast)
        self.sidebar_ui.saturation_slider.configure(command=self.tools.apply_saturation)
        self.sidebar_ui.grayscale_btn.configure(command=self.tools.apply_grayscale)
        # Add other callbacks as needed

    def open_image(self, event=None):
        self.tools.open_image()

    def save_image(self, event=None):
        self.tools.save_image()

    def display_image_on_canvas(self):
        self.tools.display_image_on_canvas()

    def resize_image(self, event=None):
        self.tools.resize_image()

    def rotate_image(self, angle):
        self.tools.rotate_image(angle)

    def flip_horizontal(self, event=None):
        self.tools.flip_horizontal()

    def flip_vertical(self, event=None):
        self.tools.flip_vertical()

    def reset_image(self, event=None):
        self.tools.reset_image()
        
    def crop_image(self):
        self.is_cropping = True
    # Filter proxies
    def apply_grayscale(self, event=None):
        self.tools.apply_grayscale()

    def apply_blur(self, event=None):
        self.tools.apply_blur()

    def apply_sharpen(self, event=None):
        self.tools.apply_sharpen()

    def apply_edge_detection(self, event=None):
        self.tools.apply_edge_detection()

    def apply_emboss(self, event=None):
        self.tools.apply_emboss()

    def apply_sepia(self, event=None):
        self.tools.apply_sepia()

    def apply_negative(self, event=None):
        self.tools.apply_negative()

    def apply_brightness(self, value):
        self.tools.apply_brightness(value)

    def apply_contrast(self, value):
        self.tools.apply_contrast(value)

    def apply_saturation(self, value):
        self.tools.apply_saturation(value)

    def on_press(self, event):
        if self.is_cropping:
            self.crop_start_x, self.crop_start_y = event.x, event.y
    
    def on_drag(self, event):
        if self.is_cropping:
            self.canvas.delete("crop_rect")
            self.crop_rect = self.canvas.create_rectangle(self.crop_start_x, self.crop_start_y, event.x, event.y, outline="red")
    
    def on_release(self, event):
        if self.is_cropping and self.crop_rect:
            # Get the final coordinates
            x1, y1, x2, y2 = self.canvas.coords(self.crop_rect)
            
            # Make sure x1 < x2 and y1 < y2
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            
            # Convert canvas coordinates to image coordinates
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            img_width, img_height = self.current_image.size
            display_width, display_height = self.display_image.size
            
            # Calculate the position of the image on the canvas
            img_x = (canvas_width - display_width) // 2
            img_y = (canvas_height - display_height) // 2
            
            # Adjust coordinates relative to the image
            x1 = max(0, x1 - img_x)
            y1 = max(0, y1 - img_y)
            x2 = min(display_width, x2 - img_x)
            y2 = min(display_height, y2 - img_y)
            
            # Scale coordinates to original image size
            scale_x = img_width / display_width
            scale_y = img_height / display_height
            
            crop_x1 = int(x1 * scale_x)
            crop_y1 = int(y1 * scale_y)
            crop_x2 = int(x2 * scale_x)
            crop_y2 = int(y2 * scale_y)
            
            # Perform the crop
            if crop_x2 > crop_x1 and crop_y2 > crop_y1:
                # Add current state to history before making changes
                self.push_to_history()
                
                self.current_image = self.current_image.crop((crop_x1, crop_y1, crop_x2, crop_y2))
                self.display_image_on_canvas()
            
            # Reset cropping state
            self.is_cropping = False
            self.canvas.delete(self.crop_rect)
            self.crop_rect = None
            self.status_bar.configure(text=f"Image cropped to {self.current_image.width}x{self.current_image.height}")

    def push_to_history(self):
        """Add current state to history"""
        if not hasattr(self, 'layer_manager') or not self.layer_manager.layers:
            return
        
        # Create a deep copy of the current layer stack
        layer_stack_copy = []
        for layer in self.layer_manager.layers:
            layer_copy = Layer(
                image=layer.image.copy() if layer.image else None,
                name=layer.name,
                visible=layer.visible,
                opacity=layer.opacity,
                blend_mode=layer.blend_mode
            )
            layer_copy.x_offset = layer.x_offset
            layer_copy.y_offset = layer.y_offset
            layer_stack_copy.append(layer_copy)
        
        # If we're not at the end of the history, truncate it
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # Add the copy to history
        self.history.append({
            'layers': layer_stack_copy,
            'active_index': self.layer_manager.active_layer_index
        })
        
        # Limit history size
        max_history = getattr(self, 'max_history_states', 20)
        if len(self.history) > max_history:
            self.history = self.history[-max_history:]
        
        # Update history index
        self.history_index = len(self.history) - 1
        
        # Update undo/redo buttons
        self.update_undo_redo_buttons()

    def clear_panel(self):
        """Clear all widgets from the properties panel."""
        # Destroy all widgets in the panel
        for widget in self.panel.winfo_children():
            widget.destroy()

    def cancel_text_editing(self, event=None):
        """Cancel the current text editing operation."""
        if hasattr(self, 'active_text_entry') and self.active_text_entry:
            self.canvas.delete(self.active_text_entry["window_id"])
            self.active_text_entry = None
            self.status_bar.configure(text="Text editing canceled")

    def create_editable_text(self, img_x, img_y, canvas_x, canvas_y):
        """Create an editable text field directly on the canvas."""
        # Get text properties from the properties panel
        text_props = self.properties_panel.text_properties
        
        # Create a text entry widget on the canvas
        text_entry = tk.Text(
            self.canvas,
            width=20,
            height=4,
            font=(text_props["font_family"], text_props["font_size"]),
            wrap="word",
            bd=0,
            highlightthickness=1,
            highlightbackground="#3584e4"
        )
        
        # Apply styling based on text properties
        if text_props["bold"] and text_props["italic"]:
            text_entry.configure(font=(text_props["font_family"], text_props["font_size"], "bold italic"))
        elif text_props["bold"]:
            text_entry.configure(font=(text_props["font_family"], text_props["font_size"], "bold"))
        elif text_props["italic"]:
            text_entry.configure(font=(text_props["font_family"], text_props["font_size"], "italic"))
        
        text_entry.configure(fg=text_props["color"], bg="transparent")
        
        # Position the text entry on the canvas
        text_window = self.canvas.create_window(
            canvas_x, canvas_y,
            window=text_entry,
            anchor="nw"
        )
        
        # Store the text entry and its position for later use
        self.active_text_entry = {
            "widget": text_entry,
            "window_id": text_window,
            "img_pos": (img_x, img_y)
        }
        
        # Focus the text entry
        text_entry.focus_set()
        
        # Bind events for finalizing text
        text_entry.bind("<FocusOut>", self.finalize_text)
        text_entry.bind("<Control-Return>", self.finalize_text)  # Ctrl+Enter to confirm
        
        # Update status
        self.status_bar.configure(text="Type your text and press Ctrl+Enter or click elsewhere to apply")

    def place_text_on_canvas(self, event):
        """Handle click event to place text at the clicked position."""
        if self.active_tool != "text" or self.current_image is None:
            return
        
        # Check if display_image exists
        if self.display_image is None:
            self.status_bar.configure(text="Please load an image first")
            return
        
        # Get click position relative to the image
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Calculate the position of the image on the canvas
        img_width, img_height = self.display_image.size
        img_x = (canvas_width - img_width) // 2
        img_y = (canvas_height - img_height) // 2
        
        # Check if click is within image bounds
        if (img_x <= event.x <= img_x + img_width and 
            img_y <= event.y <= img_y + img_height):
            
            # Calculate position relative to the image
            rel_x = event.x - img_x
            rel_y = event.y - img_y
            
            # Scale coordinates to original image size if zoomed
            if hasattr(self, 'zoom_level'):
                scale_x = self.current_image.width / img_width
                scale_y = self.current_image.height / img_height
                img_x_pos = int(rel_x * scale_x)
                img_y_pos = int(rel_y * scale_y)
            else:
                img_x_pos = rel_x
                img_y_pos = rel_y
            
            # Create an editable text field on the canvas
            self.create_editable_text(img_x_pos, img_y_pos, event.x, event.y)

    def handle_drop(self, event):
        """Handle the drop event when a file is dropped onto the canvas."""
        # Get the file path from the event
        file_path = event.data
        
        # Clean up the file path (tkinterdnd2 adds braces and may include multiple files)
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]
        
        # If multiple files were dropped, take only the first one
        if ' ' in file_path and (file_path.startswith('"') or file_path.startswith("'")):
            # This handles paths with spaces that are quoted
            import re
            match = re.match(r'["\'](.*?)["\']', file_path)
            if match:
                file_path = match.group(1)
        elif ' ' in file_path:
            # If multiple unquoted paths, take the first one
            file_path = file_path.split(' ')[0]
        
        # Check if the file is an image
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        if file_path.lower().endswith(valid_extensions):
            # Set the image path and load the image
            self.image_path = file_path
            try:
                self.original_image = Image.open(file_path)
                self.current_image = self.original_image.copy()
                self.display_image_on_canvas()
                self.status_bar.configure(text=f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open image: {str(e)}")
        else:
            messagebox.showerror("Error", "Unsupported file type. Please drop an image file.")

    def undo(self):
        """Undo the last action"""
        if not hasattr(self, 'layer_manager') or self.history_index <= 0:
            return
        
        # Move back in history
        self.history_index -= 1
        
        # Restore the state
        state = self.history[self.history_index]
        self.layer_manager.layers = state['layers']
        self.layer_manager.active_layer_index = state['active_index']
        
        # Update the display
        self.current_image = self.layer_manager.get_composite_image()
        self.display_image_on_canvas()
        
        # Update layer panel
        self.layer_panel.update_layers()
        
        # Update undo/redo buttons
        self.update_undo_redo_buttons()

    def redo(self):
        """Redo the last undone action"""
        if not hasattr(self, 'layer_manager') or self.history_index >= len(self.history) - 1:
            return
        
        # Move forward in history
        self.history_index += 1
        
        # Restore the state
        state = self.history[self.history_index]
        self.layer_manager.layers = state['layers']
        self.layer_manager.active_layer_index = state['active_index']
        
        # Update the display
        self.current_image = self.layer_manager.get_composite_image()
        self.display_image_on_canvas()
        
        # Update layer panel
        self.layer_panel.update_layers()
        
        # Update undo/redo buttons
        self.update_undo_redo_buttons()
        
    def update_undo_redo_buttons(self):
        """Update the state of undo/redo buttons based on history."""
        # Enable/disable undo button
        if self.history_index > 0:
            self.toolbar.undo_btn.configure(state="normal")
            if hasattr(self, 'edit_menu'):
                self.edit_menu.entryconfig("Undo", state="normal")
        else:
            self.toolbar.undo_btn.configure(state="disabled")
            if hasattr(self, 'edit_menu'):
                self.edit_menu.entryconfig("Undo", state="disabled")
        
        # Enable/disable redo button
        if self.history_index < len(self.history) - 1:
            self.toolbar.redo_btn.configure(state="normal")
            if hasattr(self, 'edit_menu'):
                self.edit_menu.entryconfig("Redo", state="normal")
        else:
            self.toolbar.redo_btn.configure(state="disabled")
            if hasattr(self, 'edit_menu'):
                self.edit_menu.entryconfig("Redo", state="disabled")

    def show_about(self):
        about_window = ctk.CTkToplevel(self.root)
        about_window.title("About Modern Image Editor")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        # Make dialog modal
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Add content
        title_label = ctk.CTkLabel(
            about_window, 
            text="Modern Image Editor", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        version_label = ctk.CTkLabel(
            about_window, 
            text="Version 1.0"
        )
        version_label.pack(pady=5)
        
        description_label = ctk.CTkLabel(
            about_window, 
            text="A simple, modern image editor built with Python,\nTkinter, and CustomTkinter.",
            justify="center"
        )
        description_label.pack(pady=10)
        
        copyright_label = ctk.CTkLabel(
            about_window, 
            text="© 2023 Modern Image Editor"
        )
        copyright_label.pack(pady=5)
        
        # Close button
        close_button = ctk.CTkButton(
            about_window,
            text="Close",
            command=about_window.destroy,
            width=100
        )
        close_button.pack(pady=20)
    
    def change_appearance_mode(self, new_appearance_mode):
        """
        Change the appearance mode of the application.
        
        Args:
            new_appearance_mode (str): The new appearance mode to set.
                Can be "System", "Light", or "Dark".
        """
        ctk.set_appearance_mode(new_appearance_mode)
        
        # Update the option menu selection if it exists
        if hasattr(self, 'appearance_option'):
            self.appearance_option.set(new_appearance_mode)
    
    def setup_zoom_functionality(self):
        """Set up zoom functionality with keyboard shortcuts and mouse wheel."""
        # Initialize zoom level
        self.zoom_level = 1.0
        self.zoom_step = 0.1
        self.min_zoom = 0.1
        self.max_zoom = 5.0
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-plus>", self.zoom_in)
        self.root.bind("<Control-equal>", self.zoom_in)  # For keyboards where + is on the = key
        self.root.bind("<Control-minus>", self.zoom_out)
        
        # Bind mouse wheel
        self.canvas.bind("<MouseWheel>", self.zoom_with_mouse_wheel)  # Windows
        self.canvas.bind("<Button-4>", self.zoom_with_mouse_wheel)    # Linux scroll up
        self.canvas.bind("<Button-5>", self.zoom_with_mouse_wheel)    # Linux scroll down

    def zoom_in(self, event=None):
        """Zoom in the image."""
        if not self.current_image:
            return
        
        self.zoom_level = min(self.zoom_level + self.zoom_step, self.max_zoom)
        self.apply_zoom()

    def zoom_out(self, event=None):
        """Zoom out the image."""
        if not self.current_image:
            return
        
        self.zoom_level = max(self.zoom_level - self.zoom_step, self.min_zoom)
        self.apply_zoom()

    def zoom_with_mouse_wheel(self, event):
        """Handle zoom with mouse wheel."""
        if not self.current_image:
            return
        
        # Determine zoom direction based on event
        if event.num == 4 or event.delta > 0:  # Scroll up or positive delta
            self.zoom_level = min(self.zoom_level + self.zoom_step, self.max_zoom)
        elif event.num == 5 or event.delta < 0:  # Scroll down or negative delta
            self.zoom_level = max(self.zoom_level - self.zoom_step, self.min_zoom)
        
        self.apply_zoom()

    def apply_zoom(self):
        """Apply the current zoom level to the image."""
        if not self.current_image:
            return
        
        # Calculate new dimensions
        new_width = int(self.current_image.width * self.zoom_level)
        new_height = int(self.current_image.height * self.zoom_level)
        
        # Resize the display image (not the actual image data)
        self.display_image = self.current_image.resize((new_width, new_height), Image.LANCZOS)
        
        # Update the display
        self.tk_image = ImageTk.PhotoImage(self.display_image)
        self.canvas.delete("all")
        self.canvas.create_image(
            self.canvas.winfo_width()//2, 
            self.canvas.winfo_height()//2, 
            image=self.tk_image, 
            anchor=tk.CENTER
        )
        
        # Update zoom level indicator
        self.zoom_label.configure(text=f"Zoom: {int(self.zoom_level * 100)}%")

    def setup_drag_drop(self):
        """Set up drag and drop functionality for the canvas."""
        try:
            # Import tkinterdnd2
            import tkinterdnd2
            from tkinterdnd2 import DND_FILES, TkinterDnD
            
            # Try to load the tkdnd package
            try:
                self.root.tk.call('package', 'require', 'tkdnd')
                
                # Register the canvas as a drop target
                self.canvas.drop_target_register(DND_FILES)
                
                # Bind the drop event to a callback function
                self.canvas.dnd_bind('<<Drop>>', self.handle_drop)
                
                # Update status bar to indicate drag and drop is enabled
                self.status_bar.configure(text="Ready - Drag and drop images to open")
                
            except Exception as e:
                print(f"Could not initialize drag and drop: {str(e)}")
                self.status_bar.configure(text="Ready - Drag and drop not available")
            
        except ImportError:
            # If tkinterdnd2 is not available, show a message
            print("Drag and drop functionality not available. Install tkinterdnd2 to enable.")
            self.status_bar.configure(text="Ready")

    def show_shortcuts_dialog(self, event=None):
        """Show keyboard shortcuts dialog."""
        self.keyboard_shortcuts.show_shortcuts_dialog()
        
    def activate_text_tool(self, event=None):
        """Activate the text tool and show its properties."""
        self.active_tool = "text"
        self.status_bar.configure(text="Text Tool: Click on the image to add text")
        
        # Show text properties in the properties panel
        if hasattr(self.properties_panel, 'show_text_properties'):
            self.properties_panel.show_text_properties()
        
        # Change cursor to indicate text tool is active
        self.canvas.config(cursor="xterm")  # Text cursor
        
        # Bind canvas click for text placement
        self.canvas.bind("<Button-1>", self.place_text_on_canvas)
    def activate_draw_tool(self, event=None):
        """Activate the drawing tool."""
        self.active_tool = "draw"
        self.status_bar.configure(text="Drawing Tool: Click and drag to draw")
        
        # Show drawing properties in the properties panel
        self.properties_panel.show_draw_properties()
        
        # Bind canvas events for drawing
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def start_drawing(self, event):
        """Start drawing on the canvas."""
        if self.active_tool != "draw" or self.current_image is None:
            return
        
        # Get click position relative to the image
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Calculate the position of the image on the canvas
        img_width, img_height = self.display_image.size
        img_x = (canvas_width - img_width) // 2
        img_y = (canvas_height - img_height) // 2
        
        # Check if click is within image bounds
        if (img_x <= event.x <= img_x + img_width and 
            img_y <= event.y <= img_y + img_height):
            
            # Calculate position relative to the image
            rel_x = event.x - img_x
            rel_y = event.y - img_y
            
            # Scale coordinates to original image size if zoomed
            if hasattr(self, 'zoom_level'):
                scale_x = self.current_image.width / img_width
                scale_y = self.current_image.height / img_height
                img_x_pos = int(rel_x * scale_x)
                img_y_pos = int(rel_y * scale_y)
            else:
                img_x_pos = rel_x
                img_y_pos = rel_y
            
            # Set the last point for drawing
            self.draw_last_point = (img_x_pos, img_y_pos)
            
            # Draw a single point
            if hasattr(self, 'draw_preview'):
                self.draw_preview.ellipse(
                    [(img_x_pos - self.draw_size//2, img_y_pos - self.draw_size//2),
                    (img_x_pos + self.draw_size//2, img_y_pos + self.draw_size//2)],
                    fill=self.draw_color
                )
                
                # Update display
                self.display_drawing_preview()

    def draw(self, event):
        """Continue drawing as the mouse moves."""
        if self.active_tool != "draw" or self.current_image is None or self.draw_last_point is None:
            return
        
        # Get current position relative to the image
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Calculate the position of the image on the canvas
        img_width, img_height = self.display_image.size
        img_x = (canvas_width - img_width) // 2
        img_y = (canvas_height - img_height) // 2
        
        # Check if within image bounds
        if (img_x <= event.x <= img_x + img_width and 
            img_y <= event.y <= img_y + img_height):
            
            # Calculate position relative to the image
            rel_x = event.x - img_x
            rel_y = event.y - img_y
            
            # Scale coordinates to original image size if zoomed
            if hasattr(self, 'zoom_level'):
                scale_x = self.current_image.width / img_width
                scale_y = self.current_image.height / img_height
                img_x_pos = int(rel_x * scale_x)
                img_y_pos = int(rel_y * scale_y)
            else:
                img_x_pos = rel_x
                img_y_pos = rel_y
            
            # Draw a line from last point to current point
            if hasattr(self, 'draw_preview'):
                self.draw_preview.line(
                    [self.draw_last_point, (img_x_pos, img_y_pos)],
                    fill=self.draw_color,
                    width=self.draw_size
                )
                
                # Draw a circle at the end point for smoother lines
                self.draw_preview.ellipse(
                    [(img_x_pos - self.draw_size//2, img_y_pos - self.draw_size//2),
                    (img_x_pos + self.draw_size//2, img_y_pos + self.draw_size//2)],
                    fill=self.draw_color
                )
                
                # Update the last point
                self.draw_last_point = (img_x_pos, img_y_pos)
                
                # Update display
                self.display_drawing_preview()

    def stop_drawing(self, event):
        """Stop drawing and apply changes to the image."""
        if self.active_tool != "draw" or self.current_image is None:
            return
        
        # Apply the drawing to the actual image
        self.tools.apply_drawing()
        
        # Reset drawing state
        self.draw_last_point = None

    def display_drawing_preview(self):
        """Display the drawing preview on the canvas."""
        if not hasattr(self, 'draw_overlay') or self.draw_overlay is None:
            return
        
        # Create a copy that's properly sized for display
        if hasattr(self, 'zoom_level'):
            preview_width = int(self.draw_overlay.width * self.zoom_level)
            preview_height = int(self.draw_overlay.height * self.zoom_level)
            display_preview = self.draw_overlay.resize((preview_width, preview_height), Image.LANCZOS)
        else:
            display_preview = self.draw_overlay.copy()
        
        # Update the display
        self.tk_image = ImageTk.PhotoImage(display_preview)
        self.canvas.delete("all")
        self.canvas.create_image(
            self.canvas.winfo_width()//2, 
            self.canvas.winfo_height()//2, 
            image=self.tk_image, 
            anchor=tk.CENTER
        )

    def place_text_on_canvas(self, event):
        """Handle click event to place text at the clicked position."""
        if self.active_tool != "text" or self.current_image is None:
            return
        
        # Check if display_image exists
        if self.display_image is None:
            self.status_bar.configure(text="Please load an image first")
            return
        
        # Get click position relative to the image
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Calculate the position of the image on the canvas
        img_width, img_height = self.display_image.size
        img_x = (canvas_width - img_width) // 2
        img_y = (canvas_height - img_height) // 2
        
        # Check if click is within image bounds
        if (img_x <= event.x <= img_x + img_width and 
            img_y <= event.y <= img_y + img_height):
            
            # Calculate position relative to the image
            rel_x = event.x - img_x
            rel_y = event.y - img_y
            
            # Scale coordinates to original image size if zoomed
            if hasattr(self, 'zoom_level'):
                scale_x = self.current_image.width / img_width
                scale_y = self.current_image.height / img_height
                img_x_pos = int(rel_x * scale_x)
                img_y_pos = int(rel_y * scale_y)
            else:
                img_x_pos = rel_x
                img_y_pos = rel_y
            
            # Create an editable text field on the canvas
            self.create_editable_text(img_x_pos, img_y_pos, event.x, event.y)


    def create_editable_text(self, img_x, img_y, canvas_x, canvas_y):
        """Create an editable text field directly on the canvas."""
        # Get text properties from the properties panel
        text_props = self.properties_panel.text_properties
        
        # Create a text entry widget on the canvas
        text_entry = tk.Text(
            self.canvas,
            width=20,
            height=4,
            font=(text_props["font_family"], text_props["font_size"]),
            wrap="word",
            bd=0,
            highlightthickness=1,
            highlightbackground="#3584e4"
        )
        
        # Apply styling based on text properties
        if text_props["bold"] and text_props["italic"]:
            text_entry.configure(font=(text_props["font_family"], text_props["font_size"], "bold italic"))
        elif text_props["bold"]:
            text_entry.configure(font=(text_props["font_family"], text_props["font_size"], "bold"))
        elif text_props["italic"]:
            text_entry.configure(font=(text_props["font_family"], text_props["font_size"], "italic"))
        
        text_entry.configure(fg=text_props["color"], bg="transparent")
        
        # Position the text entry on the canvas
        text_window = self.canvas.create_window(
            canvas_x, canvas_y,
            window=text_entry,
            anchor="nw"
        )
        
        # Store the text entry and its position for later use
        self.active_text_entry = {
            "widget": text_entry,
            "window_id": text_window,
            "img_pos": (img_x, img_y)
        }
        
        # Focus the text entry
        text_entry.focus_set()
        
        # Bind events for finalizing text
        text_entry.bind("<FocusOut>", self.finalize_text)
        text_entry.bind("<Control-Return>", self.finalize_text)  # Ctrl+Enter to confirm
        
        # Update status
        self.status_bar.configure(text="Type your text and press Ctrl+Enter or click elsewhere to apply")
    def finalize_text(self, event):
        """Finalize the text and apply it to the image."""
        if not hasattr(self, 'active_text_entry') or self.active_text_entry is None:
            return
        
        # Get the text from the entry widget
        text_content = self.active_text_entry["widget"].get("1.0", "end-1c")
        
        # If text is empty, just remove the widget without applying
        if not text_content.strip():
            self.canvas.delete(self.active_text_entry["window_id"])
            self.active_text_entry = None
            return
        
        # Get text properties
        text_props = self.properties_panel.text_properties
        
        # Get the position on the image
        img_x, img_y = self.active_text_entry["img_pos"]
        
        # Remove the text entry widget
        self.canvas.delete(self.active_text_entry["window_id"])
        self.active_text_entry = None
        
        # Add the text to the image
        self.add_text_to_image(
            text_content,
            text_props["font_family"],
            text_props["font_size"],
            text_props["bold"],
            text_props["italic"],
            text_props["color"],
            position=(img_x, img_y)
        )

    def cancel_text_editing(self, event=None):
        """Cancel the current text editing operation."""
        if hasattr(self, 'active_text_entry') and self.active_text_entry:
            self.canvas.delete(self.active_text_entry["window_id"])
            self.active_text_entry = None
            self.status_bar.configure(text="Text editing canceled")

    def add_text_to_image(self, text, font_family, font_size, bold, italic, color, position=None):
        """Add text to the current image."""
        if self.current_image is None:
            self.status_bar.configure(text="No image to add text to")
            return
        
        # Save current state for undo
        self.push_to_history()
        
        # Create a drawing context
        from PIL import ImageDraw, ImageFont
        import os
        
        # Create a copy of the current image
        img_copy = self.current_image.copy()
        draw = ImageDraw.Draw(img_copy)
        
        # Determine font style and try to load appropriate font
        try:
            # For simplicity, we'll use default fonts that come with PIL
            # In a real application, you'd need to handle font paths properly
            font_style = ""
            if bold and italic:
                font_style = "bold italic"
            elif bold:
                font_style = "bold"
            elif italic:
                font_style = "italic"
            
            # Try to load the font - this is simplified and may not work on all systems
            try:
                # Try to use TrueType font if available
                font = ImageFont.truetype(font_family, font_size)
            except:
                # Fall back to default font
                if bold and italic:
                    font = ImageFont.BOLD + ImageFont.ITALIC
                elif bold:
                    font = ImageFont.BOLD
                elif italic:
                    font = ImageFont.ITALIC
                else:
                    font = ImageFont.load_default()
        except Exception as e:
            print(f"Error loading font: {e}")
            font = ImageFont.load_default()
        
        # Use provided position or default to center of image
        if position is None:
            width, height = img_copy.size
            position = (width // 2, height // 2)
            anchor = "mm"  # Center the text at the position
        else:
            anchor = "lt"  # Top-left anchoring for direct placement
        
        # Draw the text
        draw.text(
            position, 
            text, 
            fill=color, 
            font=font,
            anchor=anchor
        )
        
        # Update the current image
        self.current_image = img_copy
        
        # Display the updated image
        self.display_image_on_canvas()
        
        # Update status
        self.status_bar.configure(text=f"Text added to image")

    def handle_drop(self, event):
        """Handle the drop event when a file is dropped onto the canvas."""
        # Get the file path from the event
        file_path = event.data
        
        # Clean up the file path (tkinterdnd2 adds braces and may include multiple files)
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]
        
        # If multiple files were dropped, take only the first one
        if ' ' in file_path and (file_path.startswith('"') or file_path.startswith("'")):
            # This handles paths with spaces that are quoted
            import re
            match = re.match(r'["\'](.*?)["\']', file_path)
            if match:
                file_path = match.group(1)
        elif ' ' in file_path:
            # If multiple unquoted paths, take the first one
            file_path = file_path.split(' ')[0]
        
        # Check if the file is an image
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        if file_path.lower().endswith(valid_extensions):
            # Set the image path and load the image
            self.image_path = file_path
            try:
                self.original_image = Image.open(file_path)
                self.current_image = self.original_image.copy()
                self.display_image_on_canvas()
                self.status_bar.configure(text=f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open image: {str(e)}")
        else:
            messagebox.showerror("Error", "Unsupported file type. Please drop an image file.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = ModernImageEditor(root)
    root.mainloop()