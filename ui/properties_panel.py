import tkinter as tk
import customtkinter as ctk
from tkinter import colorchooser

class PropertiesPanel:
    def __init__(self, editor, parent):
        self.editor = editor
        self.parent = parent
        self.properties_container = parent
    
        # Create the panel frame that will contain all the properties widgets
        self.panel = ctk.CTkFrame(self.parent)
        self.panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
        # Initialize with empty content or default message
        self.default_label = ctk.CTkLabel(self.panel, text="Select a tool to see its properties")
        self.default_label.pack(pady=20)

        self.empty_label = ctk.CTkLabel(self.panel, text="No tool selected")
    
    # Initialize header label
        self.header_label = ctk.CTkLabel(self.panel, text="Tool Properties", font=("Arial", 14, "bold"))
        self.header_label.pack(pady=(0, 10))
        
        # Initialize text properties frame
        self.create_text_properties()
    
        # Hide all property frames initially
        self.hide_all_properties()
    
        # Default text properties
        self.text_properties = {
            "font_family": "Arial",
            "font_size": 16,
            "bold": False,
            "italic": False,
            "color": "#000000"
        }
        self.draw_properties = {
        "color": "#FF0000",  # Default: Red
        "size": 3            # Default: 3px
        }
    def show_tool_properties(self, tool_name):
        """Show properties for the selected tool."""
        self.hide_all_properties()
        
        if tool_name == "text":
            self.show_text_properties()
        elif tool_name == "draw":
            self.show_draw_properties()
        # Add other tools as needed
        else:
            # Show default/empty panel
            self.empty_label.pack(pady=50)
            self.header_label.configure(text="Tool Properties")

    def create_text_properties(self):
        """Create properties for text tool."""
        self.text_frame = ctk.CTkFrame(self.properties_container)
        
        # Font family dropdown
        font_family_label = ctk.CTkLabel(self.text_frame, text="Font:")
        font_family_label.pack(anchor="w", pady=(10, 0), padx=10)
        
        # Get available fonts
        available_fonts = ["Arial", "Times New Roman", "Courier New", "Verdana", "Georgia"]
        
        self.font_family_var = tk.StringVar(value=available_fonts[0])
        self.font_family_dropdown = ctk.CTkOptionMenu(
            self.text_frame,
            values=available_fonts,
            variable=self.font_family_var,
            command=self.update_text_font
        )
        self.font_family_dropdown.pack(fill="x", pady=(5, 10), padx=10)
        
        # Font size slider
        font_size_label = ctk.CTkLabel(self.text_frame, text="Font Size:")
        font_size_label.pack(anchor="w", pady=(10, 0), padx=10)
        
        self.font_size_slider = ctk.CTkSlider(
            self.text_frame,
            from_=8,
            to=200,
            number_of_steps=64,
            command=self.update_font_size
        )
        self.font_size_slider.set(16)  # Default size
        self.font_size_slider.pack(fill="x", pady=(5, 10), padx=10)
        
        self.font_size_value = ctk.CTkLabel(self.text_frame, text="16 pt")
        self.font_size_value.pack(anchor="e", padx=10)
        
        # Font style checkboxes
        style_frame = ctk.CTkFrame(self.text_frame)
        style_frame.pack(fill="x", pady=(10, 0), padx=10)
        
        self.bold_var = tk.BooleanVar(value=False)
        self.bold_checkbox = ctk.CTkCheckBox(
            style_frame, 
            text="Bold",
            variable=self.bold_var,
            command=self.update_text_style
        )
        self.bold_checkbox.pack(side="left", padx=(0, 10))
        
        self.italic_var = tk.BooleanVar(value=False)
        self.italic_checkbox = ctk.CTkCheckBox(
            style_frame, 
            text="Italic",
            variable=self.italic_var,
            command=self.update_text_style
        )
        self.italic_checkbox.pack(side="left")
        
        # Text color picker
        text_color_label = ctk.CTkLabel(self.text_frame, text="Text Color:")
        text_color_label.pack(anchor="w", pady=(10, 0), padx=10)
        
        color_frame = ctk.CTkFrame(self.text_frame)
        color_frame.pack(fill="x", pady=(5, 20), padx=10)
        
        self.text_color_button = ctk.CTkButton(
            color_frame,
            text="Select Color",
            command=self.select_text_color
        )
        self.text_color_button.pack(side="left", fill="x", expand=True)
        
        # Color preview
        self.text_color_preview = tk.Canvas(
            color_frame, 
            width=30, 
            height=30, 
            bg="#000000",
            highlightthickness=1,
            highlightbackground="#555555"
        )
        self.text_color_preview.pack(side="right", padx=(10, 0))
        
        # Text input field
        text_input_label = ctk.CTkLabel(self.text_frame, text="Text Content:")
        text_input_label.pack(anchor="w", pady=(10, 0), padx=10)
        
        self.text_input = ctk.CTkTextbox(
            self.text_frame,
            height=100,
            wrap="word"
        )
        self.text_input.pack(fill="x", pady=(5, 10), padx=10)
        
        # Apply text button
        self.apply_text_button = ctk.CTkButton(
            self.text_frame,
            text="Apply Text to Image",
            command=self.apply_text_to_image
        )
        self.apply_text_button.pack(fill="x", pady=(5, 10), padx=10)
    
    def hide_all_properties(self):
        """Hide all tool property frames."""
        if hasattr(self, 'text_frame'):
            self.text_frame.pack_forget()
        
        # Show empty label
        self.empty_label.pack(pady=50)
    
    def show_text_properties(self):
        """Show text tool properties."""
        self.hide_all_properties()
        self.empty_label.pack_forget()
        self.text_frame.pack(fill="both", expand=True)
        self.header_label.configure(text="Text Tool Properties")
    
    def update_text_font(self, font_family):
        """Update the text font family."""
        self.text_properties["font_family"] = font_family
        print(f"Font family updated to: {font_family}")
    
    def update_font_size(self, size):
        """Update the text font size."""
        size = int(size)
        self.text_properties["font_size"] = size
        self.font_size_value.configure(text=f"{size} pt")
        print(f"Font size updated to: {size}")
    
    def update_text_style(self):
        """Update the text style (bold/italic)."""
        self.text_properties["bold"] = self.bold_var.get()
        self.text_properties["italic"] = self.italic_var.get()
        print(f"Text style updated - Bold: {self.text_properties['bold']}, Italic: {self.text_properties['italic']}")
    
    def select_text_color(self):
        """Open color picker and update text color."""
        color = colorchooser.askcolor(initialcolor=self.text_properties["color"])
        if color[1]:  # If a color was selected (not canceled)
            self.text_properties["color"] = color[1]
            self.text_color_preview.configure(bg=color[1])
            print(f"Text color updated to: {color[1]}")
    
    def apply_text_to_image(self):
        """Apply the text to the image."""
        text_content = self.text_input.get("1.0", "end-1c")
        if not text_content.strip():
            print("No text to add")
            return
        
        # Call the editor's method to add text to the image
        if hasattr(self.editor, 'add_text_to_image'):
            self.editor.add_text_to_image(
                text_content, 
                self.text_properties["font_family"],
                self.text_properties["font_size"],
                self.text_properties["bold"],
                self.text_properties["italic"],
                self.text_properties["color"]
            )
        else:
            print("Text tool not fully implemented in the editor")

    def show_draw_properties(self):
        """Show drawing tool properties."""
        self.hide_all_properties()
        self.empty_label.pack_forget()
        
        # Initialize draw properties if not already done
        if not hasattr(self, 'draw_properties'):
            self.draw_properties = {
                "color": "#FF0000",  # Default: Red
                "size": 3,           # Default: 3px
                "opacity": 100,      # Default: 100%
                "brush_type": "Round" # Default: Round
            }
        
        # Create color picker
        color_frame = ctk.CTkFrame(self.panel)
        color_frame.pack(fill=tk.X, padx=10, pady=5)

        color_label = ctk.CTkLabel(color_frame, text="Color:")
        color_label.pack(side=tk.LEFT, padx=5)
        
        # Create a button that opens a color chooser
        self.color_btn = ctk.CTkButton(
            color_frame, 
            text="", 
            width=30, 
            height=20, 
            fg_color=self.draw_properties["color"],
            command=self.choose_draw_color
        )
        self.color_btn.pack(side=tk.RIGHT, padx=5)
        
        # Create brush size slider
        size_frame = ctk.CTkFrame(self.panel)
        size_frame.pack(fill=tk.X, padx=10, pady=5)
        
        size_label = ctk.CTkLabel(size_frame, text="Brush Size:")
        size_label.pack(anchor="w", padx=5)
        
        self.size_slider = ctk.CTkSlider(
            size_frame,
            from_=1,
            to=20,
            number_of_steps=19,
            command=self.update_brush_size
        )
        self.size_slider.set(self.draw_properties["size"])
        self.size_slider.pack(fill=tk.X, padx=5, pady=5)
        
        # Display current size value
        self.size_value_label = ctk.CTkLabel(size_frame, text=f"{self.draw_properties['size']}px")
        self.size_value_label.pack(anchor="e", padx=5)
        
        # Create opacity slider
        opacity_frame = ctk.CTkFrame(self.panel)
        opacity_frame.pack(fill=tk.X, padx=10, pady=5)
        
        opacity_label = ctk.CTkLabel(opacity_frame, text="Opacity:")
        opacity_label.pack(anchor="w", padx=5)
        
        self.opacity_slider = ctk.CTkSlider(
            opacity_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            command=self.update_opacity
        )
        self.opacity_slider.set(self.draw_properties["opacity"])
        self.opacity_slider.pack(fill=tk.X, padx=5, pady=5)
        
        # Display current opacity value
        self.opacity_value_label = ctk.CTkLabel(opacity_frame, text=f"{self.draw_properties['opacity']}%")
        self.opacity_value_label.pack(anchor="e", padx=5)
        
        # Create brush type dropdown
        brush_type_frame = ctk.CTkFrame(self.panel)
        brush_type_frame.pack(fill=tk.X, padx=10, pady=5)
        
        brush_type_label = ctk.CTkLabel(brush_type_frame, text="Brush Type:")
        brush_type_label.pack(anchor="w", padx=5)
        
        available_brush_types = ["Round", "Square", "Diamond"]
        
        self.brush_type_var = tk.StringVar(value=self.draw_properties["brush_type"])
        self.brush_type_dropdown = ctk.CTkOptionMenu(
            brush_type_frame,
            values=available_brush_types,
            variable=self.brush_type_var,
            command=self.update_brush_type
        )
        self.brush_type_dropdown.pack(fill="x", pady=(5, 10), padx=10)
        
    def choose_draw_color(self):
        """Open color chooser dialog for drawing color."""
        from tkinter import colorchooser
        color = colorchooser.askcolor(initialcolor=self.draw_properties["color"])[1]
        if color:
            self.draw_properties["color"] = color
            self.color_btn.configure(fg_color=color)
            
            # Update active drawing color if draw tool is active
            if self.editor.active_tool == "draw":
                self.editor.draw_color = color

    def update_opacity(self, value):
        """Update the opacity for drawing."""
        opacity = int(value)
        self.draw_properties["opacity"] = opacity
        self.opacity_value_label.configure(text=f"{opacity}%")
        
        # Update active drawing opacity if draw tool is active
        if self.editor.active_tool == "draw":
            self.editor.draw_opacity = opacity
            
    def update_brush_type(self, brush_type):
        """Update the brush type for drawing."""
        self.draw_properties["brush_type"] = brush_type
        print(f"Brush type updated to: {brush_type}")
        
        # Update active drawing brush type if draw tool is active
        if self.editor.active_tool == "draw":
            self.editor.draw_brush_type = brush_type