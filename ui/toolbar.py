import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import io
import requests
import cairosvg
import json
from tkinter import filedialog, messagebox


class Toolbarr:
    def __init__(self, editor):
        self.editor = editor
        self.icons = {}  # Dictionary to store loaded icons
        self.max_recent_files = 5 
        self.load_fontawesome_icons()
        self.create_toolbar()
    

    def load_fontawesome_icons(self):
        """Load FontAwesome icons for the toolbar buttons"""
        # Define FontAwesome CDN URLs for the icons we need
        fa_icons = {
            "open": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/folder-open.svg",
            "save": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/save.svg",
            "undo": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/undo.svg",
            "redo": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/redo.svg",
            "crop": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/crop.svg",
            "resize": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/expand.svg",
            "rotate": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/rotate.svg",
            "flip": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/arrows-left-right.svg",
            "filters": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/filter.svg",
            "draw": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/pen.svg",
        }
        
        # Create a cache directory for icons
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons")
        os.makedirs(cache_dir, exist_ok=True)
        
        # Icon size for toolbar buttons
        icon_size = (20, 20)  # Standard size for toolbar buttons
        
        # Download and process each icon
        for name, url in fa_icons.items():
            svg_path = os.path.join(cache_dir, f"{name}.svg")
            png_path = os.path.join(cache_dir, f"{name}.png")
            
            # Check if we already have the SVG cached
            if not os.path.exists(svg_path):
                try:
                    # Download the SVG
                    response = requests.get(url)
                    if response.status_code == 200:
                        # Save the SVG file
                        with open(svg_path, 'wb') as f:
                            f.write(response.content)
                    else:
                        print(f"Failed to download {name} icon: HTTP {response.status_code}")
                        continue
                except Exception as e:
                    print(f"Error downloading {name} icon: {e}")
                    continue
            
            try:
                # Convert SVG to PNG if not already done
                if not os.path.exists(png_path):
                    # Convert SVG to PNG with white fill for icons
                    with open(svg_path, 'r') as f:
                        svg_data = f.read()
                    
                    # Replace currentColor with white for better visibility on dark buttons
                    svg_data = svg_data.replace('fill="currentColor"', 'fill="white"')
                    
                    # Convert to PNG using cairosvg
                    cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), 
                                     write_to=png_path,
                                     output_width=64, 
                                     output_height=64)
                
                # Load the PNG and create CTkImage
                pil_image = Image.open(png_path).resize(icon_size, Image.LANCZOS)
                self.icons[name] = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=icon_size
                )
            except Exception as e:
                print(f"Error processing {name} icon: {e}")
    
    def create_toolbar(self):
        # Create toolbar frame directly on the root window
        self.toolbar_frame = ctk.CTkFrame(self.editor.root, height=40)
        
        # Pack it at the TOP of the window BEFORE the main_frame
        self.toolbar_frame.pack(fill=tk.X, side=tk.TOP, padx=10, pady=(10, 0))
        
        # Define button width and padding
        btn_width = 80
        btn_padding = 5
        # Edit operations
        self.undo_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Undo", 
            image=self.icons.get("undo"),
            compound="left",
            command=self.editor.undo,
            width=btn_width,
            height=30,
            state="disabled"
        )
        self.undo_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        self.redo_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Redo", 
            image=self.icons.get("redo"),
            compound="left",
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
            image=self.icons.get("crop"),
            compound="left",
            command=self.editor.crop_image,
            width=btn_width,
            height=30
        )
        self.crop_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        self.resize_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Resize", 
            image=self.icons.get("resize"),
            compound="left",
            command=self.editor.resize_image,
            width=btn_width,
            height=30
        )
        self.resize_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        self.rotate_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Rotate", 
            image=self.icons.get("rotate"),
            compound="left",
            command=lambda: self.editor.rotate_image(90),
            width=btn_width,
            height=30
        )
        self.rotate_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        self.flip_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Flip", 
            image=self.icons.get("flip"),
            compound="left",
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
            image=self.icons.get("filters"),
            compound="left",
            command=lambda: None,  # Placeholder for filters
            width=btn_width,
            height=30
        )
        self.filters_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)
        
        self.draw_btn = ctk.CTkButton(
            self.toolbar_frame, 
            text="Draw", 
            image=self.icons.get("draw"),
            compound="left",
            command=self.editor.activate_draw_tool if hasattr(self.editor, 'activate_draw_tool') else lambda: None,
            width=btn_width,
            height=30
        )
        self.draw_btn.pack(side=tk.LEFT, padx=btn_padding, pady=btn_padding)

    def show_file_menu(self, widget):
        """Show the file menu below the file button"""
        try:
            x = widget.winfo_rootx()
            y = widget.winfo_rooty() + widget.winfo_height()
            self.file_menu.tk_popup(x, y)
        finally:
            # Make sure to release the grab
            self.file_menu.grab_release()

    def get_tk_image(self, icon_name):
        """Convert CTkImage to Tkinter PhotoImage for menu items"""
        if icon_name in self.icons:
            # Get the PIL image from the CTkImage
            pil_image = self.icons[icon_name]._light_image
            
            # Convert to PhotoImage
            return ImageTk.PhotoImage(pil_image)
        return None
