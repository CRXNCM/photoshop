import tkinter as tk

class MenuManager:
    def __init__(self, editor):
        self.editor = editor
        self.create_menu()
    
    def create_menu(self):
        # Create main menu bar
        self.menu_bar = tk.Menu(self.editor.root)
        self.editor.root.config(menu=self.menu_bar)
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open...", command=self.editor.open_image, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.editor.save_image, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As...", command=lambda: self.editor.save_image(save_as=True), accelerator="Ctrl+Shift+S")
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

        self.filters_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Filters", menu=self.filters_menu)
        self.filters_menu.add_command(label="Grayscale", command=self.editor.apply_grayscale, accelerator="G")
        self.filters_menu.add_command(label="Blur", command=self.editor.apply_blur, accelerator="Ctrl+B")
        self.filters_menu.add_command(label="Sharpen", command=self.editor.apply_sharpen, accelerator="Ctrl+S")
        self.filters_menu.add_command(label="Edge Detection", command=self.editor.apply_edge_detection)
        self.filters_menu.add_command(label="Emboss", command=self.editor.apply_emboss)
        # Add this line after creating the filters_menu


        
        # Tools menu
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Pencil", command=self.editor.keyboard_shortcuts.activate_pencil_tool, accelerator="P")
        self.tools_menu.add_command(label="Brush", command=self.editor.keyboard_shortcuts.activate_brush_tool, accelerator="B")
        self.tools_menu.add_command(label="Eraser", command=self.editor.keyboard_shortcuts.activate_eraser_tool, accelerator="E")
        self.tools_menu.add_command(label="Text", command=self.editor.keyboard_shortcuts.activate_text_tool, accelerator="T")
        self.tools_menu.add_command(label="Color Picker", command=lambda: None)
        self.tools_menu.add_separator()        
        
        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Keyboard Shortcuts", command=self.editor.keyboard_shortcuts.show_shortcuts_dialog, accelerator="F1")
        self.help_menu.add_command(label="About", command=self.editor.show_about)
