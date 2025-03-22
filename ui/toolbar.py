import tkinter as tk
import customtkinter as ctk

class Toolbarr:
    def __init__(self, editor):
        self.editor = editor
        self.create_toolbar()
    
    def create_toolbar(self):
        # Create toolbar frame directly on the root window
        # This ensures it's at the top level of the UI hierarchy
        self.toolbar_frame = ctk.CTkFrame(self.editor.root, height=40)
        
        # Pack it at the TOP of the window BEFORE the main_frame
        # This is the key change to ensure it appears above everything else
        self.toolbar_frame.pack(fill=tk.X, side=tk.TOP, padx=10, pady=(10, 0))
        
        # Define button width and padding
        btn_width = 80
        btn_padding = 5
        
        # File operations
        self.open_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Open", 
            command=self.editor.open_image,
            width=btn_width,
            height=30
        )
        self.open_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        self.save_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Save", 
            command=self.editor.save_image,
            width=btn_width,
            height=30
        )
        self.save_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        # Separator
        ctk.CTkFrame(self.toolbar_frame, width=1, height=30).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Edit operations
        self.undo_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Undo", 
            command=self.editor.undo,
            width=btn_width,
            height=30,
            state="disabled"
        )
        self.undo_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        self.redo_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Redo", 
            command=self.editor.redo,
            width=btn_width,
            height=30,
            state="disabled"
        )
        self.redo_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        # Separator
        ctk.CTkFrame(self.toolbar_frame, width=1, height=30).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Image operations
        self.crop_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Crop", 
            command=self.editor.crop_image,
            width=btn_width,
            height=30
        )
        self.crop_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        self.resize_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Resize", 
            command=self.editor.resize_image,
            width=btn_width,
            height=30
        )
        self.resize_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        self.rotate_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Rotate", 
            command=lambda: self.editor.rotate_image(90),
            width=btn_width,
            height=30
        )
        self.rotate_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        self.flip_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Flip", 
            command=self.editor.flip_horizontal,
            width=btn_width,
            height=30
        )
        self.flip_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        # Separator
        ctk.CTkFrame(self.toolbar_frame, width=1, height=30).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Additional tools
        self.filters_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Filters", 
            command=lambda: None,  # Placeholder for filters
            width=btn_width,
            height=30
        )
        self.filters_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        self.draw_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Draw", 
            command=lambda: None,  # Placeholder for draw
            width=btn_width,
            height=30
        )
        self.draw_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)