import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import io
import requests
import cairosvg
import json
from tkinter import filedialog, messagebox
from ui.settings_manager import SettingsManager


class MenuManager:
    def __init__(self, editor):
        self.editor = editor
        self.recent_files = self.load_recent_files()
        self.max_recent_files = 5

        self.settings_manager = self.editor.SettingsManager
        self.create_menu()
    
    def load_recent_files(self):
        """Load the list of recent files from a JSON file"""
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
        os.makedirs(config_dir, exist_ok=True)
        
        recent_files_path = os.path.join(config_dir, "recent_files.json")
        
        if os.path.exists(recent_files_path):
            try:
                with open(recent_files_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading recent files: {e}")
                return []
        return []
    
    def save_recent_files(self):
        """Save the list of recent files to a JSON file"""
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
        os.makedirs(config_dir, exist_ok=True)
        
        recent_files_path = os.path.join(config_dir, "recent_files.json")
        
        try:
            with open(recent_files_path, 'w') as f:
                json.dump(self.recent_files, f)
        except Exception as e:
            print(f"Error saving recent files: {e}")
    
    def add_to_recent_files(self, filepath):
        """Add a file to the recent files list"""
        if filepath in self.recent_files:
            # Move to the top if already exists
            self.recent_files.remove(filepath)
        
        # Add to the beginning of the list
        self.recent_files.insert(0, filepath)
        
        # Trim the list if it exceeds the maximum
        if len(self.recent_files) > self.max_recent_files:
            self.recent_files = self.recent_files[:self.max_recent_files]
        
        # Save the updated list
        self.save_recent_files()
        
        # Update the recent files menu
        self.update_recent_files_menu()
    
    def update_recent_files_menu(self):
        """Update the recent files menu with current list"""
        # Clear existing menu items
        self.recent_menu.delete(0, 'end')
        
        if not self.recent_files:
            # Add a disabled item if no recent files
            self.recent_menu.add_command(label="No recent files", state="disabled")
        else:
            # Add each recent file to the menu
            for filepath in self.recent_files:
                # Get just the filename for display
                filename = os.path.basename(filepath)
                self.recent_menu.add_command(
                    label=filename,
                    command=lambda f=filepath: self.open_recent_file(f)
                )
            
            # Add separator and clear option
            self.recent_menu.add_separator()
            self.recent_menu.add_command(
                label="Clear Recent Files",
                command=self.clear_recent_files
            )
    
    def open_recent_file(self, filepath):
        """Open a file from the recent files list"""
        if os.path.exists(filepath):
            self.editor.open_image_from_path(filepath)
        else:
            # If file doesn't exist, remove it from the list
            self.recent_files.remove(filepath)
            self.save_recent_files()
            self.update_recent_files_menu()
            messagebox.showerror("Error", f"File not found: {filepath}")
    
    def clear_recent_files(self):
        """Clear the recent files list"""
        self.recent_files = []
        self.save_recent_files()
        self.update_recent_files_menu()
    
    def new_image(self):
        """Create a new blank image dialog"""
        self.editor.new_image()
    
    def export_image(self):
        """Export the current image in different formats"""
        self.editor.export_image()
    
    def create_menu(self):
        # Create main menu bar
        self.menu_bar = tk.Menu(self.editor.root)
        self.editor.root.config(menu=self.menu_bar)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # Add New command
        self.file_menu.add_command(label="New...", command=self.new_image, accelerator="Ctrl+N")
        
        # Add Open command
        self.file_menu.add_command(label="Open...", command=self.editor.open_image, accelerator="Ctrl+O")
        
        # Create Recent Files submenu
        self.recent_menu = tk.Menu(self.file_menu, tearoff=0)
        self.file_menu.add_cascade(label="Open Recent", menu=self.recent_menu)
        self.update_recent_files_menu()  # Populate with recent files
        
        self.file_menu.add_separator()
        
        # Add Save commands
        self.file_menu.add_command(label="Save", command=self.editor.save_image, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As...", command=lambda: self.editor.save_image(save_as=True), accelerator="Ctrl+Shift+S")
        
        # Add Export command
        self.file_menu.add_command(label="Export As...", command=self.export_image, accelerator="Ctrl+E")
        
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.editor.root.quit, accelerator="Ctrl+Q")
        
        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.editor.undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.editor.redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Crop", command=self.editor.crop_image, accelerator="C")
        self.edit_menu.add_command(label="Resize", command=self.editor.resize_image, accelerator="R")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Reset to Original", command=self.editor.reset_image, accelerator="Ctrl+0")
        
        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Zoom In", command=self.editor.zoom_in, accelerator="Ctrl++")
        self.view_menu.add_command(label="Zoom Out", command=self.editor.zoom_out, accelerator="Ctrl+-")
        self.view_menu.add_command(label="Reset Zoom", command=lambda: self.editor.set_zoom(100), accelerator="Ctrl+1")
        
        # Image menu
        self.image_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Image", menu=self.image_menu)
        self.image_menu.add_command(label="Rotate Left", command=lambda: self.editor.rotate_image(-90), accelerator="Left Arrow")
        self.image_menu.add_command(label="Rotate Right", command=lambda: self.editor.rotate_image(90), accelerator="Right Arrow")
        self.image_menu.add_command(label="Flip Horizontal", command=self.editor.flip_horizontal, accelerator="F")
        self.image_menu.add_command(label="Flip Vertical", command=self.editor.flip_vertical, accelerator="Shift+F")

        # Filters menu
        self.filters_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Filters", menu=self.filters_menu)
        self.filters_menu.add_command(label="Grayscale", command=self.editor.tools.apply_grayscale, accelerator="G")
        self.filters_menu.add_command(label="Blur", command=self.editor.tools.apply_blur, accelerator="Ctrl+B")
        self.filters_menu.add_command(label="Sharpen", command=self.editor.tools.apply_sharpen, accelerator="Ctrl+S")
        self.filters_menu.add_command(label="Edge Detection", command=self.editor.tools.apply_edge_detection)
        self.filters_menu.add_command(label="Emboss", command=self.editor.tools.apply_emboss)
        self.filters_menu.add_command(label="Negative", command=self.editor.tools.apply_negative)
        self.filters_menu.add_command(label="Sepia", command=self.editor.tools.apply_sepia)
        
        ## Tools menu
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Pencil", command=self.editor.keyboard_shortcuts.activate_pencil_tool, accelerator="P")
        self.tools_menu.add_command(label="Brush", command=self.editor.keyboard_shortcuts.activate_brush_tool, accelerator="B")
        self.tools_menu.add_command(label="Eraser", command=self.editor.keyboard_shortcuts.activate_eraser_tool, accelerator="E")
        self.tools_menu.add_command(label="Text", command=self.editor.keyboard_shortcuts.activate_text_tool, accelerator="T")
        self.tools_menu.add_command(label="Color Picker", command=lambda: None)
        self.tools_menu.add_separator()        
        
        # Settings menu - Add this new menu
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Preferences...", command=self.open_settings_dialog, accelerator="Ctrl+,")
        
        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Keyboard Shortcuts", command=self.editor.keyboard_shortcuts.show_shortcuts_dialog, accelerator="F1")
        self.help_menu.add_command(label="About", command=self.editor.show_about)

    def open_settings_dialog(self):
        """Open the settings dialog window"""
        self.settings_manager.show_settings_dialog()
    def load_recent_files(self):
        """Load the list of recent files from a JSON file"""
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
        os.makedirs(config_dir, exist_ok=True)
        
        recent_files_path = os.path.join(config_dir, "recent_files.json")
        
        if os.path.exists(recent_files_path):
            try:
                with open(recent_files_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading recent files: {e}")
                return []
        return []
    
    def save_recent_files(self):
        """Save the list of recent files to a JSON file"""
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
        os.makedirs(config_dir, exist_ok=True)
        
        recent_files_path = os.path.join(config_dir, "recent_files.json")
        
        try:
            with open(recent_files_path, 'w') as f:
                json.dump(self.recent_files, f)
        except Exception as e:
            print(f"Error saving recent files: {e}")
    
    def add_to_recent_files(self, filepath):
        """Add a file to the recent files list"""
        if filepath in self.recent_files:
            # Move to the top if already exists
            self.recent_files.remove(filepath)
        
        # Add to the beginning of the list
        self.recent_files.insert(0, filepath)
        
        # Trim the list if it exceeds the maximum
        if len(self.recent_files) > self.max_recent_files:
            self.recent_files = self.recent_files[:self.max_recent_files]
        
        # Save the updated list
        self.save_recent_files()
        
        # Update the recent files menu
        self.update_recent_files_menu()
    
    def update_recent_files_menu(self):
        """Update the recent files menu with current list"""
        # Clear existing menu items
        self.recent_menu.delete(0, 'end')
        
        if not self.recent_files:
            # Add a disabled item if no recent files
            self.recent_menu.add_command(label="No recent files", state="disabled")
        else:
            # Add each recent file to the menu
            for filepath in self.recent_files:
                # Get just the filename for display
                filename = os.path.basename(filepath)
                self.recent_menu.add_command(
                    label=filename,
                    command=lambda f=filepath: self.open_recent_file(f)
                )
            
            # Add separator and clear option
            self.recent_menu.add_separator()
            self.recent_menu.add_command(
                label="Clear Recent Files",
                command=self.clear_recent_files
            )
    
    def open_recent_file(self, filepath):
        """Open a file from the recent files list"""
        if os.path.exists(filepath):
            self.editor.open_image_from_path(filepath)
        else:
            # If file doesn't exist, remove it from the list
            self.recent_files.remove(filepath)
            self.save_recent_files()
            self.update_recent_files_menu()
            messagebox.showerror("Error", f"File not found: {filepath}")
            
    def open_image_from_path(self, filepath):
        """Open an image from a specific file path"""
        try:
            # Load the image
            image = Image.open(filepath)
            
            # Store the image
            self.current_image = image
            self.original_image = image.copy()
            self.image_path = filepath
            
            # Clear history
            self.history = []
            self.history_index = -1
            
            # Display the image
            self.display_image_on_canvas()
            
            # Update UI state
            self.update_ui_state()
            
            # Add to recent files
            if hasattr(self.toolbar, 'add_to_recent_files'):
                self.toolbar.add_to_recent_files(filepath)
            
            # Update status
            self.status_bar.configure(text=f"Opened: {filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {str(e)}")

    def clear_recent_files(self):
        """Clear the recent files list"""
        self.recent_files = []
        self.save_recent_files()
        self.update_recent_files_menu()
    
    def new_image(self):
        """Create a new blank image"""
        # Create a dialog to get dimensions
        new_window = ctk.CTkToplevel(self.editor.root)
        new_window.title("New Image")
        new_window.geometry("300x200")
        new_window.resizable(False, False)
        new_window.transient(self.editor.root)  # Make it a modal dialog
        new_window.grab_set()
        
        # Center the window
        new_window.update_idletasks()
        width = new_window.winfo_width()
        height = new_window.winfo_height()
        x = (new_window.winfo_screenwidth() // 2) - (width // 2)
        y = (new_window.winfo_screenheight() // 2) - (height // 2)
        new_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Width input
        width_frame = ctk.CTkFrame(new_window)
        width_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        width_label = ctk.CTkLabel(width_frame, text="Width:")
        width_label.pack(side=tk.LEFT, padx=(0, 10))
        
        width_var = tk.StringVar(value="800")
        width_entry = ctk.CTkEntry(width_frame, textvariable=width_var)
        width_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Height input
        height_frame = ctk.CTkFrame(new_window)
        height_frame.pack(fill=tk.X, padx=20, pady=10)
        
        height_label = ctk.CTkLabel(height_frame, text="Height:")
        height_label.pack(side=tk.LEFT, padx=(0, 10))
        
        height_var = tk.StringVar(value="600")
        height_entry = ctk.CTkEntry(height_frame, textvariable=height_var)
        height_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Background color
        color_frame = ctk.CTkFrame(new_window)
        color_frame.pack(fill=tk.X, padx=20, pady=10)
        
        color_label = ctk.CTkLabel(color_frame, text="Background:")
        color_label.pack(side=tk.LEFT, padx=(0, 10))
        
        color_var = tk.StringVar(value="white")
        color_options = ["white", "black", "transparent"]
        color_dropdown = ctk.CTkOptionMenu(color_frame, values=color_options, variable=color_var)
        color_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Buttons
        button_frame = ctk.CTkFrame(new_window)
        button_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        def create_image():
            try:
                width = int(width_var.get())
                height = int(height_var.get())
                bg_color = color_var.get()
                
                # Validate dimensions
                if width <= 0 or height <= 0 or width > 5000 or height > 5000:
                    messagebox.showerror("Error", "Invalid dimensions. Width and height must be between 1 and 5000 pixels.")
                    return
                
                # Create the new image
                if bg_color == "transparent":
                    new_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
                else:
                    new_image = Image.new("RGB", (width, height), bg_color)
                
                # Set it as the current image
                self.editor.current_image = new_image
                self.editor.original_image = new_image.copy()
                self.editor.image_path = None
                self.editor.history = []
                self.editor.history_index = -1
                
                # Display the new image
                self.editor.display_image_on_canvas()
                
                # Update UI state
                self.editor.update_ui_state()
                
                # Close the dialog
                new_window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Width and height must be valid numbers.")
        
        cancel_btn = ctk.CTkButton(
            button_frame, 
            text="Cancel", 
            command=new_window.destroy,
            width=80
        )
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        create_btn = ctk.CTkButton(
            button_frame, 
            text="Create", 
            command=create_image,
            width=80
        )
        create_btn.pack(side=tk.RIGHT)
    
    def export_image(self):
        """Export the current image in different formats"""
        if not self.editor.current_image:
            messagebox.showinfo("Info", "Please open or create an image first")
            return
        
        # Get file path from user
        file_types = [
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg *.jpeg"),
            ("BMP Image", "*.bmp"),
            ("GIF Image", "*.gif"),
            ("TIFF Image", "*.tiff *.tif"),
            ("All Files", "*.*")
        ]
        
        filepath = filedialog.asksaveasfilename(
            title="Export Image As",
            filetypes=file_types,
            defaultextension=".png"
        )
        
        if not filepath:
            return  # User cancelled
        
        try:
            # Get file extension
            _, ext = os.path.splitext(filepath)
            ext = ext.lower()
            
            # Handle different formats
            if ext == '.jpg' or ext == '.jpeg':
                # Convert to RGB if needed (JPEG doesn't support alpha)
                if self.editor.current_image.mode == 'RGBA':
                    rgb_image = Image.new('RGB', self.editor.current_image.size, (255, 255, 255))
                    rgb_image.paste(self.editor.current_image, mask=self.editor.current_image.split()[3])
                    rgb_image.save(filepath, 'JPEG', quality=95)
                else:
                    self.editor.current_image.save(filepath, 'JPEG', quality=95)
            else:
                # Save in the requested format
                self.editor.current_image.save(filepath)
            
            messagebox.showinfo("Success", f"Image exported successfully to {filepath}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export image: {str(e)}")
    