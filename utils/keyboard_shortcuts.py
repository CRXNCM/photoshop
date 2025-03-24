import tkinter as tk
import customtkinter as ctk
from layers.layer import Layer
from layers.layer_manager import LayerManager
from ui.layer_panel import LayerPanel
class KeyboardShortcuts:
    def __init__(self, editor):
        self.editor = editor
        self.setup_shortcuts()
    
    def setup_shortcuts(self):
        """Set up all keyboard shortcuts for the application."""
        # File operations
        self.editor.root.bind("<Control-o>", self.editor.open_image)
        self.editor.root.bind("<Control-s>", self.editor.save_image)
        self.editor.root.bind("<Control-Shift-s>", lambda e: self.editor.save_image(save_as=True))
        self.editor.root.bind("<Control-q>", lambda e: self.editor.root.quit())
        
        # Edit operations
        self.editor.root.bind("<Control-z>", self.editor.undo)
        self.editor.root.bind("<Control-y>", self.editor.redo)
        self.editor.root.bind("<Control-0>", self.editor.reset_image)
        
        # Image transformations
        self.editor.root.bind("c", self.editor.crop_image)
        self.editor.root.bind("r", self.editor.resize_image)
        self.editor.root.bind("<Left>", lambda e: self.editor.rotate_image(-90))
        self.editor.root.bind("<Right>", lambda e: self.editor.rotate_image(90))
        self.editor.root.bind("f", self.editor.flip_horizontal)
        self.editor.root.bind("<Shift-f>", self.editor.flip_vertical)
        
        # Tools
        self.editor.root.bind("p", self.activate_pencil_tool)
        self.editor.root.bind("b", self.activate_brush_tool)
        self.editor.root.bind("e", self.activate_eraser_tool)
        self.editor.root.bind("t", self.activate_text_tool)
        
        # Filters
        self.editor.root.bind("g", self.editor.apply_grayscale)
        self.editor.root.bind("<Control-b>", lambda e: self.editor.apply_blur())
        self.editor.root.bind("<Control-h>", lambda e: self.editor.apply_sharpen())
        # In the setup_shortcuts method
        # Layer shortcuts
        self.editor.root.bind("<Shift-Control-n>", lambda e: self.editor.layer_manager.add_layer())
        self.editor.root.bind("<Shift-Control-d>", lambda e: self.editor.layer_manager.duplicate_layer())
        self.editor.root.bind("<Shift-Control-Delete>", lambda e: self.editor.layer_manager.delete_layer())
        self.editor.root.bind("<Control-e>", lambda e: self.editor.layer_manager.merge_with_below())
        self.editor.root.bind("<Shift-Control-e>", lambda e: self.editor.layer_manager.flatten_image())

                
        # View
        self.editor.root.bind("<Control-plus>", lambda e: self.editor.zoom_in())
        self.editor.root.bind("<Control-minus>", lambda e: self.editor.zoom_out())
        self.editor.root.bind("<Control-1>", lambda e: self.editor.set_zoom(100))
        
        # Help
        # Change this line
        self.editor.root.bind("F1", self.show_shortcuts_dialog)

    
    def activate_pencil_tool(self, event=None):
        """Activate the pencil tool."""
        if hasattr(self.editor, 'sidebar_ui') and hasattr(self.editor.sidebar_ui, 'pencil_btn'):
            self.editor.sidebar_ui.pencil_btn.invoke()
    
    def activate_brush_tool(self, event=None):
        """Activate the brush tool."""
        if hasattr(self.editor, 'sidebar_ui') and hasattr(self.editor.sidebar_ui, 'brush_btn'):
            self.editor.sidebar_ui.brush_btn.invoke()
    
    def activate_eraser_tool(self, event=None):
        """Activate the eraser tool."""
        if hasattr(self.editor, 'sidebar_ui') and hasattr(self.editor.sidebar_ui, 'eraser_btn'):
            self.editor.sidebar_ui.eraser_btn.invoke()
    
    def activate_text_tool(self, event=None):
        """Activate the text tool."""
        if hasattr(self.editor, 'sidebar_ui') and hasattr(self.editor.sidebar_ui, 'text_btn'):
            self.editor.sidebar_ui.text_btn.invoke()
    
    def show_shortcuts_dialog(self, event=None):
        """Display a dialog with all keyboard shortcuts."""
        shortcuts_window = ctk.CTkToplevel(self.editor.root)
        shortcuts_window.title("Keyboard Shortcuts")
        shortcuts_window.geometry("500x600")
        shortcuts_window.resizable(False, False)
        
        # Make dialog modal
        shortcuts_window.transient(self.editor.root)
        shortcuts_window.grab_set()
        
        # Add content
        title_label = ctk.CTkLabel(
            shortcuts_window, 
            text="Keyboard Shortcuts", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Create a scrollable frame for the shortcuts
        scrollable_frame = ctk.CTkScrollableFrame(shortcuts_window, width=450, height=450)
        scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Add shortcuts by category
        self.add_shortcut_category(scrollable_frame, "File Operations", [
            ("Open", "Ctrl+O"),
            ("Save", "Ctrl+S"),
            ("Save As", "Ctrl+Shift+S"),
            ("Exit", "Ctrl+Q")
        ])
        
        self.add_shortcut_category(scrollable_frame, "Edit Operations", [
            ("Undo", "Ctrl+Z"),
            ("Redo", "Ctrl+Y"),
            ("Reset to Original", "Ctrl+0")
        ])
        
        self.add_shortcut_category(scrollable_frame, "Image Transformations", [
            ("Crop", "C"),
            ("Resize", "R"),
            ("Rotate Left", "Left Arrow"),
            ("Rotate Right", "Right Arrow"),
            ("Flip Horizontal", "F"),
            ("Flip Vertical", "Shift+F")
        ])
        
        self.add_shortcut_category(scrollable_frame, "Tools", [
            ("Pencil Tool", "P"),
            ("Brush Tool", "B"),
            ("Eraser Tool", "E"),
            ("Text Tool", "T")
        ])
        
        self.add_shortcut_category(scrollable_frame, "Filters", [
            ("Grayscale", "G"),
            ("Blur", "Ctrl+B"),
            ("Sharpen", "Ctrl+S")
        ])
        
        self.add_shortcut_category(scrollable_frame, "View", [
            ("Zoom In", "Ctrl++"),
            ("Zoom Out", "Ctrl+-"),
            ("Reset Zoom", "Ctrl+1")
        ])
        
        self.add_shortcut_category(scrollable_frame, "Help", [
            ("Show Keyboard Shortcuts", "F1")
        ])
        
        # Close button
        close_button = ctk.CTkButton(
            shortcuts_window,
            text="Close",
            command=shortcuts_window.destroy,
            width=100
        )
        close_button.pack(pady=20)
    
    def add_shortcut_category(self, parent, category_name, shortcuts):
        """Add a category of shortcuts to the parent widget."""
        # Category label
        category_label = ctk.CTkLabel(
            parent, 
            text=category_name, 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        category_label.pack(anchor="w", pady=(10, 5))
        
        # Shortcuts frame
        shortcuts_frame = ctk.CTkFrame(parent)
        shortcuts_frame.pack(fill="x", pady=(0, 10))
        
        # Add each shortcut
        for i, (action, shortcut) in enumerate(shortcuts):
            action_label = ctk.CTkLabel(shortcuts_frame, text=action, anchor="w")
            action_label.grid(row=i, column=0, sticky="w", padx=(10, 20), pady=2)
            
            shortcut_label = ctk.CTkLabel(shortcuts_frame, text=shortcut, anchor="e")
            shortcut_label.grid(row=i, column=1, sticky="e", padx=(20, 10), pady=2)
