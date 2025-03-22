import tkinter as tk
import customtkinter as ctk
from tkinter import colorchooser

class PropertiesPanel:
    def __init__(self, editor, parent_frame):
        self.editor = editor
        self.parent_frame = parent_frame
        
        # Create main frame for properties panel
        self.frame = ctk.CTkFrame(parent_frame, width=450)
        self.frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))
        
        # Create header
        self.header_label = ctk.CTkLabel(
            self.frame, 
            text="Tool Properties", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.header_label.pack(pady=(10, 15), padx=10)
        
        # Create container for tool-specific properties
        self.properties_container = ctk.CTkFrame(self.frame)
        self.properties_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create empty label for when no tool is selected
        self.empty_label = ctk.CTkLabel(
            self.properties_container,
            text="Select a tool",
            wraplength=220
        )
        self.empty_label.pack(pady=50)
        
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
            to=72,
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
