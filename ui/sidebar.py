import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import io
import requests
import cairosvg  # You'll need to install this: pip install cairosvg

class Sidebar:
    def __init__(self, editor):
        self.editor = editor
        self.icons = {}  # Dictionary to store loaded icons
        self.load_fontawesome_icons()
        self.create_sidebar()
    
    def load_fontawesome_icons(self):
        """Load FontAwesome icons for the sidebar buttons"""
        # Define FontAwesome CDN URLs for the icons we need
        fa_icons = {
            "pencil": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/pencil.svg",
            "brush": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/paint-brush.svg",
            "eraser": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/eraser.svg",
            "text": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/font.svg",
            "draw": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/pen.svg",
            "grayscale": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/adjust.svg",
            "reset": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/undo.svg",
            "brightness": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/sun.svg",
            "contrast": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/adjust.svg",
            "saturation": "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free/svgs/solid/palette.svg",
        }
        
        # Create a cache directory for icons
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons")
        os.makedirs(cache_dir, exist_ok=True)
        
        # Icon sizes for different UI elements
        icon_sizes = {
            "button": (20, 20),      # Size for buttons
            "slider": (16, 16),      # Smaller for slider labels
            "action": (24, 24)       # Larger for action buttons
        }
        
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
                
                # Load the PNG and create CTkImage in different sizes
                for size_name, dimensions in icon_sizes.items():
                    pil_image = Image.open(png_path).resize(dimensions, Image.LANCZOS)
                    self.icons[f"{name}_{size_name}"] = ctk.CTkImage(
                        light_image=pil_image,
                        dark_image=pil_image,
                        size=dimensions
                    )
            except Exception as e:
                print(f"Error processing {name} icon: {e}")
    
    def create_sidebar(self):
        # App title
        self.app_title = ctk.CTkLabel(
            self.editor.sidebar, 
            text="Image Editor", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.app_title.pack(pady=(20, 30))
        
        # Tools section
        self.tools_frame = ctk.CTkFrame(self.editor.sidebar)
        self.tools_frame.pack(fill=tk.X, padx=10, pady=(0, 20))
        
        self.tools_label = ctk.CTkLabel(
            self.tools_frame, 
            text="Tools", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.tools_label.pack(anchor="w", pady=(0, 5))
        
        # Tool buttons in a grid (2x2)
        self.tools_grid = ctk.CTkFrame(self.tools_frame)
        self.tools_grid.pack(fill=tk.X, pady=5)
        
        # Row 1
        self.pencil_btn = ctk.CTkButton(
            self.tools_grid, 
            text="Pencil", 
            image=self.icons.get("pencil_button"),
            compound="left",
            command=lambda: None,
            height=32,
            width=100
        )
        self.pencil_btn.grid(row=0, column=0, padx=5, pady=5)

        self.brush_btn = ctk.CTkButton(
            self.tools_grid, 
            text="Brush", 
            image=self.icons.get("brush_button"),
            compound="left",
            command=lambda: None,
            height=32,
            width=100
        )
        self.brush_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Row 2
        self.eraser_btn = ctk.CTkButton(
            self.tools_grid, 
            text="Eraser", 
            image=self.icons.get("eraser_button"),
            compound="left",
            command=lambda: None,
            height=32,
            width=100
        )
        self.eraser_btn.grid(row=1, column=0, padx=5, pady=5)
        
        self.text_btn = ctk.CTkButton(
            self.tools_grid, 
            text="Text", 
            image=self.icons.get("text_button"),
            compound="left",
            command=self.editor.activate_text_tool if hasattr(self.editor, 'activate_text_tool') else lambda: None,
            height=32,
            width=100
        )
        self.text_btn.grid(row=1, column=1, padx=5, pady=5)
        
        # Draw button
        self.draw_btn = ctk.CTkButton(
            self.tools_frame,
            text="Draw",
            image=self.icons.get("draw_button"),
            compound="left",
            command=self.editor.activate_draw_tool,
            height=32
        )
        self.draw_btn.pack(fill=tk.X, padx=5, pady=2)
        
        # Color adjustments section
        self.adjustments_frame = ctk.CTkFrame(self.editor.sidebar)
        self.adjustments_frame.pack(fill=tk.X, padx=10, pady=(0, 20))
        
        self.adjustments_label = ctk.CTkLabel(
            self.adjustments_frame, 
            text="Color Adjustments", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.adjustments_label.pack(anchor="w", pady=(0, 10))
        
        # Brightness adjustment with icon
        self.brightness_frame = ctk.CTkFrame(self.adjustments_frame)
        self.brightness_frame.pack(fill=tk.X, pady=(5, 0))
        
        if "brightness_slider" in self.icons:
            self.brightness_icon = ctk.CTkLabel(
                self.brightness_frame,
                text="",
                image=self.icons["brightness_slider"],
                width=16
            )
            self.brightness_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        self.brightness_label = ctk.CTkLabel(self.brightness_frame, text="Brightness:")
        self.brightness_label.pack(side=tk.LEFT, pady=(5, 0))
        
        self.brightness_slider = ctk.CTkSlider(
            self.adjustments_frame,
            from_=-100,
            to=100,
            number_of_steps=200,
            command=self.editor.tools.apply_brightness
        )
        self.brightness_slider.pack(fill=tk.X, pady=(0, 10))
        self.brightness_slider.set(0)  # Default value
        
        # Contrast adjustment with icon
        self.contrast_frame = ctk.CTkFrame(self.adjustments_frame)
        self.contrast_frame.pack(fill=tk.X, pady=(5, 0))
        
        if "contrast_slider" in self.icons:
            self.contrast_icon = ctk.CTkLabel(
                self.contrast_frame,
                text="",
                image=self.icons["contrast_slider"],
                width=16
            )
            self.contrast_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        self.contrast_label = ctk.CTkLabel(self.contrast_frame, text="Contrast:")
        self.contrast_label.pack(side=tk.LEFT, pady=(5, 0))
        
        self.contrast_slider = ctk.CTkSlider(
            self.adjustments_frame,
            from_=-100,
            to=100,
            number_of_steps=200,
            command=self.editor.tools.apply_contrast
        )
        self.contrast_slider.pack(fill=tk.X, pady=(0, 10))
        self.contrast_slider.set(0)  # Default value
        
        # Saturation adjustment with icon
        self.saturation_frame = ctk.CTkFrame(self.adjustments_frame)
        self.saturation_frame.pack(fill=tk.X, pady=(5, 0))
        
        if "saturation_slider" in self.icons:
            self.saturation_icon = ctk.CTkLabel(
                self.saturation_frame,
                text="",
                image=self.icons["saturation_slider"],
                width=16
            )
            self.saturation_icon.pack(side=tk.LEFT, padx=(0, 5))
        
        self.saturation_label = ctk.CTkLabel(self.saturation_frame, text="Saturation:")
        self.saturation_label.pack(side=tk.LEFT, pady=(5, 0))
        
        self.saturation_slider = ctk.CTkSlider(
            self.adjustments_frame,
            from_=-100,
            to=100,
            number_of_steps=200,
            command=self.editor.tools.apply_saturation
        )
        self.saturation_slider.pack(fill=tk.X, pady=(0, 10))
        self.saturation_slider.set(0)  # Default value
        
        # Grayscale button
        self.grayscale_btn = ctk.CTkButton(
            self.adjustments_frame, 
            text="Grayscale", 
            image=self.icons.get("grayscale_button"),
            compound="left",
            command=self.editor.tools.apply_grayscale,
            height=32
        )
        self.grayscale_btn.pack(fill=tk.X, pady=5)
        
        # Reset button
        self.reset_btn = ctk.CTkButton(
            self.editor.sidebar, 
            text="Reset to Original", 
            image=self.icons.get("reset_action"),
            compound="left",
            command=self.editor.reset_image if hasattr(self.editor, 'reset_image') else lambda: None,
            fg_color="#E74C3C",  # Red color for reset button
            hover_color="#C0392B",
            height=40
        )
        self.reset_btn.pack(fill=tk.X, padx=10, pady=(20, 10))
        
        # Appearance mode
        self.appearance_label = ctk.CTkLabel(
            self.editor.sidebar, 
            text="Appearance Mode:", 
            anchor="w"
        )
        self.appearance_label.pack(padx=10, pady=(20, 0), anchor="w")
        
        self.appearance_option = ctk.CTkOptionMenu(
            self.editor.sidebar,
            values=["System", "Light", "Dark"],
            command=self.editor.change_appearance_mode if hasattr(self.editor, 'change_appearance_mode') else lambda x: None
        )
        self.appearance_option.pack(padx=10, pady=(5, 10), fill=tk.X)
        self.appearance_option.set("System")
