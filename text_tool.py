import tkinter as tk
import customtkinter as ctk
from tkinter import colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk

class TextTool:
    """A class to handle text addition and manipulation in an image editor."""
    
    def __init__(self, parent, canvas, status_bar, push_to_history_callback, display_image_callback):
        """
        Initialize the text tool.
        
        Args:
            parent: The parent window/frame
            canvas: The canvas where the image is displayed
            status_bar: The status bar to show messages
            push_to_history_callback: Function to call to save state for undo
            display_image_callback: Function to call to update the canvas
        """
        self.parent = parent
        self.canvas = canvas
        self.status_bar = status_bar
        self.push_to_history = push_to_history_callback
        self.display_image = display_image_callback
        
        # Text tool state variables
        self.is_text_mode = False
        self.text_dialog = None
        self.text_position = (0, 0)
        self.text_content = "Sample Text"
        self.text_color = "#FFFFFF"  # Default: white
        self.text_font = "Arial"
        self.text_size = 24
        self.text_bold = False
        self.text_italic = False
        self.text_rotation = 0
        self.text_alignment = "left"  # Options: left, center, right
        
        # Text effects
        self.text_shadow = False
        self.text_shadow_color = "#000000"
        self.text_shadow_offset = (2, 2)
        
        # Text background
        self.text_background = False
        self.text_background_color = "#000000"
        self.text_background_opacity = 128  # 0-255
        self.text_padding = 10  # Padding around text
        
        # Text objects for editing
        self.text_objects = []
        self.selected_text_object = None
        self.dragging_text = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # Current image reference (will be set when needed)
        self.current_image = None
    
    def activate(self, current_image):
        """
        Activate the text tool.
        
        Args:
            current_image: The current image being edited
        """
        if current_image is None:
            ctk.CTkMessagebox(
                title="Info", 
                message="Please open an image first",
                icon="info"
            )
            return
        
        self.current_image = current_image
        self.is_text_mode = True
        self.status_bar.configure(text="Text Tool: Click on the image to place text")
        
        # Show text configuration dialog
        self.show_config_dialog()
    
    def show_config_dialog(self, edit_mode=False):
        """Show dialog to configure text properties."""
        # Create a toplevel window
        self.text_dialog = ctk.CTkToplevel(self.parent)
        self.text_dialog.title("Text Properties")
        self.text_dialog.geometry("450x650")
        self.text_dialog.resizable(False, False)
        
        # Make dialog modal
        self.text_dialog.transient(self.parent)
        self.text_dialog.grab_set()
        
        # Create a scrollable frame for all content
        scroll_frame = ctk.CTkScrollableFrame(self.text_dialog, width=430, height=580)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text content
        text_content_frame = ctk.CTkFrame(scroll_frame)
        text_content_frame.pack(fill=tk.X, pady=(0, 10))
        
        text_content_label = ctk.CTkLabel(
            text_content_frame, 
            text="Text:", 
            font=ctk.CTkFont(size=14)
        )
        text_content_label.pack(anchor="w", pady=(0, 5))
        
        self.text_entry = ctk.CTkTextbox(
            text_content_frame,
            height=80,
            wrap="word"
        )
        self.text_entry.pack(fill=tk.X, pady=(0, 10))
        self.text_entry.insert("1.0", self.text_content)
        
        # Font selection
        font_frame = ctk.CTkFrame(scroll_frame)
        font_frame.pack(fill=tk.X, pady=10)
        
        font_label = ctk.CTkLabel(
            font_frame, 
            text="Font:", 
            font=ctk.CTkFont(size=14)
        )
        font_label.pack(anchor="w", pady=(0, 5))
        
        # Get available fonts
        available_fonts = ["Arial", "Times New Roman", "Courier New", "Verdana", "Georgia", "Tahoma", "Trebuchet MS"]
        
        self.font_option = ctk.CTkOptionMenu(
            font_frame,
            values=available_fonts,
            command=self.update_text_preview
        )
        self.font_option.pack(fill=tk.X, pady=(0, 10))
        self.font_option.set(self.text_font)
        
        # Font size
        size_frame = ctk.CTkFrame(scroll_frame)
        size_frame.pack(fill=tk.X, pady=10)
        
        size_label = ctk.CTkLabel(
            size_frame, 
            text="Size:", 
            font=ctk.CTkFont(size=14)
        )
        size_label.pack(anchor="w", pady=(0, 5))
        
        size_slider_frame = ctk.CTkFrame(size_frame)
        size_slider_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.size_slider = ctk.CTkSlider(
            size_slider_frame,
            from_=8,
            to=72,
            number_of_steps=64,
            command=self.update_text_size
        )
        self.size_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.size_slider.set(self.text_size)
        
        self.size_label = ctk.CTkLabel(
            size_slider_frame, 
            text=f"{self.text_size}",
            width=30
        )
        self.size_label.pack(side=tk.RIGHT)
        
        # Text style (bold, italic)
        style_frame = ctk.CTkFrame(scroll_frame)
        style_frame.pack(fill=tk.X, pady=10)
        
        style_label = ctk.CTkLabel(
            style_frame, 
            text="Style:", 
            font=ctk.CTkFont(size=14)
        )
        style_label.pack(anchor="w", pady=(0, 5))
        
        style_buttons_frame = ctk.CTkFrame(style_frame)
        style_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.bold_var = tk.BooleanVar(value=self.text_bold)
        self.bold_checkbox = ctk.CTkCheckBox(
            style_buttons_frame,
            text="Bold",
            variable=self.bold_var,
            command=self.update_text_preview
        )
        self.bold_checkbox.pack(side=tk.LEFT, padx=(0, 20))
        
        self.italic_var = tk.BooleanVar(value=self.text_italic)
        self.italic_checkbox = ctk.CTkCheckBox(
            style_buttons_frame,
            text="Italic",
            variable=self.italic_var,
            command=self.update_text_preview
        )
        self.italic_checkbox.pack(side=tk.LEFT)
        
        # Text alignment
        alignment_frame = ctk.CTkFrame(scroll_frame)
        alignment_frame.pack(fill=tk.X, pady=10)
        
        alignment_label = ctk.CTkLabel(
            alignment_frame, 
            text="Alignment:", 
            font=ctk.CTkFont(size=14)
        )
        alignment_label.pack(anchor="w", pady=(0, 5))
        
        self.alignment_var = tk.StringVar(value=self.text_alignment)
        
        alignment_buttons_frame = ctk.CTkFrame(alignment_frame)
        alignment_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        alignment_left = ctk.CTkRadioButton(
            alignment_buttons_frame,
            text="Left",
            variable=self.alignment_var,
            value="left",
            command=self.update_text_preview
        )
        alignment_left.pack(side=tk.LEFT, padx=(0, 10))
        
        alignment_center = ctk.CTkRadioButton(
            alignment_buttons_frame,
            text="Center",
            variable=self.alignment_var,
            value="center",
            command=self.update_text_preview
        )
        alignment_center.pack(side=tk.LEFT, padx=(0, 10))
        
        alignment_right = ctk.CTkRadioButton(
            alignment_buttons_frame,
            text="Right",
            variable=self.alignment_var,
            value="right",
            command=self.update_text_preview
        )
        alignment_right.pack(side=tk.LEFT)
        
        # Text rotation
        rotation_frame = ctk.CTkFrame(scroll_frame)
        rotation_frame.pack(fill=tk.X, pady=10)
        
        rotation_label = ctk.CTkLabel(
            rotation_frame, 
            text="Rotation:", 
            font=ctk.CTkFont(size=14)
        )
        rotation_label.pack(anchor="w", pady=(0, 5))
        
        rotation_slider_frame = ctk.CTkFrame(rotation_frame)
        rotation_slider_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.rotation_slider = ctk.CTkSlider(
            rotation_slider_frame,
            from_=0,
            to=360,
            number_of_steps=36,
            command=self.update_text_rotation
        )
        self.rotation_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.rotation_slider.set(self.text_rotation)
        
        self.rotation_label = ctk.CTkLabel(
            rotation_slider_frame, 
            text=f"{self.text_rotation}°",
            width=40
        )
        self.rotation_label.pack(side=tk.RIGHT)
        
        # Text color
        color_frame = ctk.CTkFrame(scroll_frame)
        color_frame.pack(fill=tk.X, pady=10)
        
        color_label = ctk.CTkLabel(
            color_frame, 
            text="Text Color:", 
            font=ctk.CTkFont(size=14)
        )
        color_label.pack(anchor="w", pady=(0, 5))
        
        self.color_button = ctk.CTkButton(
            color_frame,
            text="Select Color",
            command=self.select_text_color
        )
        self.color_button.pack(fill=tk.X, pady=(0, 10))
        
        # Color preview
        self.color_preview = tk.Canvas(
            color_frame,
            width=380,
            height=30,
            bg=self.text_color,
            highlightthickness=1,
            highlightbackground="#555555"
        )
        self.color_preview.pack(fill=tk.X, pady=(0, 10))
        
        # Text background
        background_frame = ctk.CTkFrame(scroll_frame)
        background_frame.pack(fill=tk.X, pady=10)
        
        background_label = ctk.CTkLabel(
            background_frame, 
            text="Background:", 
            font=ctk.CTkFont(size=14)
        )
        background_label.pack(anchor="w", pady=(0, 5))
        
        self.background_var = tk.BooleanVar(value=self.text_background)
        self.background_checkbox = ctk.CTkCheckBox(
            background_frame,
            text="Enable Background",
            variable=self.background_var,
            command=self.update_text_preview
        )
        self.background_checkbox.pack(anchor="w", pady=(0, 10))
        
        background_color_frame = ctk.CTkFrame(background_frame)
        background_color_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.background_color_button = ctk.CTkButton(
            background_color_frame,
            text="Background Color",
            command=self.select_background_color,
            width=150
        )
        self.background_color_button.pack(side=tk.LEFT)
        
        self.background_preview = tk.Canvas(
            background_color_frame,
            width=30,
            height=30,
            bg=self.text_background_color,
            highlightthickness=1,
            highlightbackground="#555555"
        )
        self.background_preview.pack(side=tk.RIGHT)
        
        # Background opacity
        opacity_frame = ctk.CTkFrame(background_frame)
        opacity_frame.pack(fill=tk.X, pady=(0, 10))
        
        opacity_label = ctk.CTkLabel(
            opacity_frame, 
            text="Opacity:", 
            width=70
        )
        opacity_label.pack(side=tk.LEFT)
        
        self.opacity_slider = ctk.CTkSlider(
            opacity_frame,
            from_=0,
            to=255,
            number_of_steps=255,
            command=self.update_background_opacity
        )
        self.opacity_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.opacity_slider.set(self.text_background_opacity)
        
        self.opacity_label = ctk.CTkLabel(
            opacity_frame, 
            text=f"{int(self.text_background_opacity/255*100)}%",
            width=40
        )
        self.opacity_label.pack(side=tk.RIGHT)
        
        # Text shadow
        shadow_frame = ctk.CTkFrame(scroll_frame)
        shadow_frame.pack(fill=tk.X, pady=10)
        
        shadow_label = ctk.CTkLabel(
            shadow_frame, 
            text="Shadow:", 
            font=ctk.CTkFont(size=14)
        )
        shadow_label.pack(anchor="w", pady=(0, 5))
        
        self.shadow_var = tk.BooleanVar(value=self.text_shadow)
        self.shadow_checkbox = ctk.CTkCheckBox(
            shadow_frame,
            text="Enable Shadow",
            variable=self.shadow_var,
            command=self.update_text_preview
        )
        self.shadow_checkbox.pack(anchor="w", pady=(0, 10))
        
        shadow_color_frame = ctk.CTkFrame(shadow_frame)
        shadow_color_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.shadow_color_button = ctk.CTkButton(
            shadow_color_frame,
            text="Shadow Color",
            command=self.select_shadow_color,
            width=150
        )
        self.shadow_color_button.pack(side=tk.LEFT)
        
        self.shadow_preview = tk.Canvas(
            shadow_color_frame,
            width=30,
            height=30,
            bg=self.text_shadow_color,
            highlightthickness=1,
            highlightbackground="#555555"
        )
        self.shadow_preview.pack(side=tk.RIGHT)
        
        # Buttons
        buttons_frame = ctk.CTkFrame(self.text_dialog)
        buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=self.cancel_text_tool,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            width=100
        )
        cancel_button.pack(side=tk.LEFT, padx=(0, 10))
        
        apply_button = ctk.CTkButton(
            buttons_frame,
            text="Apply",
            command=self.apply_text_config,
            width=100
        )
        apply_button.pack(side=tk.RIGHT)
        
        # Create text preview if in edit mode
        if edit_mode:
            self.create_text_preview()
    
    def update_text_size(self, value):
        """Update the text size value."""
        self.text_size = int(value)
        self.size_label.configure(text=f"{self.text_size}")
        self.update_text_preview()
    
    def update_text_rotation(self, value):
        """Update the text rotation value."""
        self.text_rotation = int(value)
        self.rotation_label.configure(text=f"{self.text_rotation}°")
        self.update_text_preview()
    
    def update_background_opacity(self, value):
        """Update the background opacity value."""
        self.text_background_opacity = int(value)
        percent = int(self.text_background_opacity / 255 * 100)
        self.opacity_label.configure(text=f"{percent}%")
        self.update_text_preview()
    
    def select_text_color(self):
        """Open color picker to select text color."""
        color = colorchooser.askcolor(initialcolor=self.text_color)
        if color[1]:  # If a color was selected
            self.text_color = color[1]
            self.color_preview.configure(bg=self.text_color)
            self.update_text_preview()
    
    def select_background_color(self):
        """Open color picker to select background color."""
        color = colorchooser.askcolor(initialcolor=self.text_background_color)
        if color[1]:  # If a color was selected
            self.text_background_color = color[1]
            self.background_preview.configure(bg=self.text_background_color)
            self.update_text_preview()
    
    def select_shadow_color(self):
        """Open color picker to select shadow color."""
        color = colorchooser.askcolor(initialcolor=self.text_shadow_color)
        if color[1]:  # If a color was selected
            self.text_shadow_color = color[1]
            self.shadow_preview.configure(bg=self.text_shadow_color)
            self.update_text_preview()
    
    def update_text_preview(self, *args):
        """Update text preview based on current settings."""
        self.text_font = self.font_option.get()
        self.text_bold = self.bold_var.get()
        self.text_italic = self.italic_var.get()
        self.text_alignment = self.alignment_var.get()
        self.text_background = self.background_var.get()
        self.text_shadow = self.shadow_var.get()
        
        # Update preview if needed
        if hasattr(self, 'text_preview_canvas'):
            self.draw_text_preview()
    
    def create_text_preview(self):
        """Create a preview canvas for the text."""
        preview_frame = ctk.CTkFrame(self.text_dialog)
        preview_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        preview_label = ctk.CTkLabel(
            preview_frame, 
            text="Preview:", 
            font=ctk.CTkFont(size=14)
        )
        preview_label.pack(anchor="w", pady=(0, 5))
        
        self.text_preview_canvas = tk.Canvas(
            preview_frame,
            width=380,
            height=100,
            bg="#2a2d2e",
            highlightthickness=1,
            highlightbackground="#555555"
        )
        self.text_preview_canvas.pack(fill=tk.X, pady=(0, 10))
        
        self.draw_text_preview()
    
    def draw_text_preview(self):
        """Draw text preview on the preview canvas."""
        self.text_preview_canvas.delete("all")
        
        # Get the text content
        text = self.text_entry.get("1.0", "end-1c")
        if not text:
            return
        
        # Create a temporary image for preview
        preview_img = Image.new('RGBA', (380, 100), (42, 45, 46, 255))
        draw = ImageDraw.Draw(preview_img)
        
        # Determine font style
        font_style = ""
        if self.text_bold:
            font_style += "bold "
        if self.text_italic:
            font_style += "italic "
        
        try:
            # Try to use the specified font
            font = ImageFont.truetype(f"{self.text_font}.ttf", self.text_size)
        except IOError:
            # Fallback to default font
            try:
                if font_style:
                    font = ImageFont.truetype("arial.ttf", self.text_size)
                else:
                    font = ImageFont.truetype("arial.ttf", self.text_size)
            except:
                # If all else fails, use default
                font = ImageFont.load_default()
        
        # Calculate text position based on alignment
        text_width, text_height = draw.textsize(text, font=font)
        x = 10  # Default left alignment
        
        if self.text_alignment == "center":
            x = (380 - text_width) // 2
        elif self.text_alignment == "right":
            x = 380 - text_width - 10
        
        y = (100 - text_height) // 2
        
        # Draw background if enabled
        if self.text_background:
            bg_color = self.text_background_color
            # Convert hex to RGBA
            r = int(bg_color[1:3], 16)
            g = int(bg_color[3:5], 16)
            b = int(bg_color[5:7], 16)
            a = self.text_background_opacity
            
            padding = self.text_padding
            draw.rectangle(
                [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
                fill=(r, g, b, a)
            )
        
        # Draw shadow if enabled
        if self.text_shadow:
            shadow_color = self.text_shadow_color
            shadow_x = x + self.text_shadow_offset[0]
            shadow_y = y + self.text_shadow_offset[1]
            draw.text((shadow_x, shadow_y), text, font=font, fill=shadow_color)
        
        # Draw the text
        draw.text((x, y), text, font=font, fill=self.text_color)
        
        # Convert to PhotoImage and display
        self.preview_photo = ImageTk.PhotoImage(preview_img)
        self.text_preview_canvas.create_image(190, 50, image=self.preview_photo)
    
    def apply_text_config(self):
        """Apply the text configuration and close the dialog."""
        # Get the text content from the text entry
        self.text_content = self.text_entry.get("1.0", "end-1c")
        
        # Close the dialog
        self.text_dialog.destroy()
        
        # Update status
        self.status_bar.configure(text="Click on the image to place text")
    
    def cancel_text_tool(self):
        """Cancel the text tool operation."""
        self.is_text_mode = False
        self.text_dialog.destroy()
        self.status_bar.configure(text="Ready")
    
    def on_canvas_click(self, event):
        """Handle canvas click events for text placement."""
        if self.is_text_mode and self.current_image:
            # Get the click position
            self.text_position = (event.x, event.y)
            
            # Add the text to the image
            self.add_text_to_image()
            
            # Deactivate text mode
            self.is_text_mode = False
            self.status_bar.configure(text="Text added")
    
    def add_text_to_image(self):
        """Add text to the current image at the specified position."""
        if not self.current_image:
            return
        
        # Create a copy of the current image
        self.push_to_history()  # Add current state to history for undo
        
        # Create a drawing context
        img_copy = self.current_image.copy()
        draw = ImageDraw.Draw(img_copy)
        
        # Determine font style
        font_style = ""
        if self.text_bold:
            font_style += "bold "
        if self.text_italic:
            font_style += "italic "
        
        try:
            # Try to use the specified font
            font = ImageFont.truetype(f"{self.text_font}.ttf", self.text_size)
        except IOError:
            # Fallback to default font
            try:
                if font_style:
                    font = ImageFont.truetype("arial.ttf", self.text_size)
                else:
                    font = ImageFont.truetype("arial.ttf", self.text_size)
            except:
                # If all else fails, use default
                font = ImageFont.load_default()
        
        # Calculate position (adjust for canvas vs image coordinates)
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_width, img_height = self.current_image.size
        
        # Calculate scaling factors
        scale_x = img_width / canvas_width
        scale_y = img_height / canvas_height
        
        # Adjust position based on scaling
        x = int(self.text_position[0] * scale_x)
        y = int(self.text_position[1] * scale_y)
        
        # Calculate text dimensions
        text_width, text_height = draw.textsize(self.text_content, font=font)
        
        # Adjust position based on alignment
        if self.text_alignment == "center":
            x -= text_width // 2
        elif self.text_alignment == "right":
            x -= text_width
        
        # Create a transparent layer for rotated text if needed
        if self.text_rotation != 0 or self.text_background or self.text_shadow:
            # Create a transparent image for the text
            text_layer = Image.new('RGBA', img_copy.size, (0, 0, 0, 0))
            text_draw = ImageDraw.Draw(text_layer)
            
            # Draw background if enabled
            if self.text_background:
                bg_color = self.text_background_color
                # Convert hex to RGBA
                r = int(bg_color[1:3], 16)
                g = int(bg_color[3:5], 16)
                b = int(bg_color[5:7], 16)
                a = self.text_background_opacity
                
                padding = self.text_padding
                text_draw.rectangle(
                    [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
                    fill=(r, g, b, a)
                )
            
            # Draw shadow if enabled
            if self.text_shadow:
                shadow_color = self.text_shadow_color
                shadow_x = x + self.text_shadow_offset[0]
                shadow_y = y + self.text_shadow_offset[1]
                text_draw.text((shadow_x, shadow_y), self.text_content, font=font, fill=shadow_color)
            
            # Draw the text
            text_draw.text((x, y), self.text_content, font=font, fill=self.text_color)
            
            # Rotate the text layer if needed
            if self.text_rotation != 0:
                # Calculate the center of the text
                text_center_x = x + text_width // 2
                text_center_y = y + text_height // 2
                
                # Rotate around the text center
                text_layer = text_layer.rotate(
                    -self.text_rotation,  # Negative because PIL rotates counter-clockwise
                    center=(text_center_x, text_center_y),
                    resample=Image.BICUBIC,
                    expand=False
                )
            
            # Composite the text layer onto the image
            img_copy = Image.alpha_composite(img_copy.convert('RGBA'), text_layer)
        else:
            # Simple case: just draw the text directly
            draw.text((x, y), self.text_content, font=font, fill=self.text_color)
        
        # Update the current image
        self.current_image = img_copy
        self.display_image(self.current_image)
