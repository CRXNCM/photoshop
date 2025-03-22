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
        
        self.tools = Toolss(self)
        self.create_ui()
        self.menu_manager.create_menu()  # Add this line
        self.setup_drag_drop()
        self.setup_zoom_functionality()
        self.tools = Toolss(self)

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

    def __init__(self, root):
        self.root = root
        self.root.title("Modern Image Editor")
        self.root.geometry("1200x700")
        
        self.image_path = None
        self.original_image = None
        self.current_image = None
        self.display_image = None
        
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_rect = None
        self.is_cropping = False
        
        # Initialize undo/redo history
        self.history = []
        self.history_index = -1
        self.max_history = 20  # Maximum number of states to keep in history
        
        self.tools = Toolss(self)
        self.create_ui()
        self.tools = Toolss(self)
        
        # Connect sidebar callbacks after tools are created
        self.connect_sidebar_callbacks()
        self.menu_manager.create_menu()  # Add this line
        self.setup_drag_drop()
        self.setup_zoom_functionality()

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
        """Add current state to history."""
        if self.current_image is None:
            return
            
        # If we're not at the end of the history, truncate it
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # Add current state to history
        self.history.append(self.current_image.copy())
        self.history_index = len(self.history) - 1
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.history_index -= 1
        
        # Update UI
        self.update_undo_redo_buttons()

    def undo(self, event=None):
        """Undo the last action."""
        if self.history_index > 0:
            self.history_index -= 1
            self.current_image = self.history[self.history_index].copy()
            self.display_image_on_canvas()
            self.status_bar.configure(text="Undo performed")
            self.update_undo_redo_buttons()

    def redo(self, event=None):
        """Redo the last undone action."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_image = self.history[self.history_index].copy()
            self.display_image_on_canvas()
            self.status_bar.configure(text="Redo performed")
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
        self.properties_panel.show_text_properties()
        
        # Change cursor to indicate text tool is active
        self.canvas.config(cursor="xterm")  # Text cursor

    def add_text_to_image(self, text, font_family, font_size, bold, italic, color):
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
            # For a production app, you'd need to handle font loading more robustly
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
        
        # For now, we'll add text at the center of the image
        # In a real application, you'd want to let the user click to position the text
        width, height = img_copy.size
        position = (width // 2, height // 2)
        
        # Draw the text
        draw.text(
            position, 
            text, 
            fill=color, 
            font=font,
            anchor="mm"  # Center the text at the position
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