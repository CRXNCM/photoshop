import tkinter as tk
import customtkinter as ctk

class Sidebar:
    def __init__(self, editor):
        self.editor = editor
        self.create_sidebar()
    
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
            command=lambda: None,
            height=32,
            width=100
        )
        self.pencil_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.brush_btn = ctk.CTkButton(
            self.tools_grid, 
            text="Brush", 
            command=lambda: None,
            height=32,
            width=100
        )
        self.brush_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Row 2
        self.eraser_btn = ctk.CTkButton(
            self.tools_grid, 
            text="Eraser", 
            command=lambda: None,
            height=32,
            width=100
        )
        self.eraser_btn.grid(row=1, column=0, padx=5, pady=5)
        
        self.text_btn = ctk.CTkButton(
            self.tools_grid, 
            text="Text", 
            command=self.editor.activate_text_tool if hasattr(self.editor, 'activate_text_tool') else lambda: None,
            height=32,
            width=100
        )
        self.text_btn.grid(row=1, column=1, padx=5, pady=5)
        
        # Color adjustments section
        self.adjustments_frame = ctk.CTkFrame(self.editor.sidebar)
        self.adjustments_frame.pack(fill=tk.X, padx=10, pady=(0, 20))
        
        self.adjustments_label = ctk.CTkLabel(
            self.adjustments_frame, 
            text="Color Adjustments", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.adjustments_label.pack(anchor="w", pady=(0, 10))
        
        # Brightness adjustment
        self.brightness_label = ctk.CTkLabel(self.adjustments_frame, text="Brightness:")
        self.brightness_label.pack(anchor="w", pady=(5, 0))
        
        self.brightness_slider = ctk.CTkSlider(
            self.adjustments_frame,
            from_=-100,
            to=100,
            number_of_steps=200,
            command=self.editor.tools.apply_brightness  # Placeholder for brightness adjustment
        )
        self.brightness_slider.pack(fill=tk.X, pady=(0, 10))
        self.brightness_slider.set(0)  # Default value
        
        # Contrast adjustment
        self.contrast_label = ctk.CTkLabel(self.adjustments_frame, text="Contrast:")
        self.contrast_label.pack(anchor="w", pady=(5, 0))
        
        self.contrast_slider = ctk.CTkSlider(
            self.adjustments_frame,
            from_=-100,
            to=100,
            number_of_steps=200,
            command=self.editor.tools.apply_contrast  # Placeholder for contrast adjustment
        )
        self.contrast_slider.pack(fill=tk.X, pady=(0, 10))
        self.contrast_slider.set(0)  # Default value
        
        # Saturation adjustment
        self.saturation_label = ctk.CTkLabel(self.adjustments_frame, text="Saturation:")
        self.saturation_label.pack(anchor="w", pady=(5, 0))
        
        self.saturation_slider = ctk.CTkSlider(
            self.adjustments_frame,
            from_=-100,
            to=100,
            number_of_steps=200,
            command=self.editor.tools.apply_saturation  # Placeholder for saturation adjustment
        )
        self.saturation_slider.pack(fill=tk.X, pady=(0, 10))
        self.saturation_slider.set(0)  # Default value
        
        # Grayscale button
        self.grayscale_btn = ctk.CTkButton(
            self.adjustments_frame, 
            text="Grayscale", 
            command=self.editor.tools.apply_grayscale,  # Placeholder for grayscale
            height=32
        )
        self.grayscale_btn.pack(fill=tk.X, pady=5)
        
        # Reset button
        self.reset_btn = ctk.CTkButton(
            self.editor.sidebar, 
            text="Reset to Original", 
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