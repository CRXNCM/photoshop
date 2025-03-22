import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
import customtkinter as ctk
import tkinter as tk
class Toolss:
    def __init__(self, editor):
        self.editor = editor
    
    def open_image(self):
        self.editor.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
    
        if self.editor.image_path:
            try:
                self.editor.original_image = Image.open(self.editor.image_path)
                self.editor.current_image = self.editor.original_image.copy()
                self.display_image_on_canvas()
                self.editor.status_bar.configure(text=f"Loaded: {os.path.basename(self.editor.image_path)}")
            
                # Clear history when opening a new image
                self.editor.history = [self.editor.current_image.copy()]
                self.editor.history_index = 0
                self.editor.update_undo_redo_buttons()
            
            except Exception as e:
                messagebox.showerror("Error", f"Could not open image: {str(e)}")
    
    def save_image(self):
        if self.editor.current_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            if file_path:
                self.editor.current_image.save(file_path)
                self.editor.status_bar.configure(text=f"Saved: {os.path.basename(file_path)}")
    
    def display_image_on_canvas(self):
        if self.editor.current_image:
            self.editor.tk_image = ImageTk.PhotoImage(self.editor.current_image)
            self.editor.canvas.delete("all")
            self.editor.canvas.create_image(
                self.editor.canvas.winfo_width()//2, 
                self.editor.canvas.winfo_height()//2, 
                image=self.editor.tk_image, 
                anchor="center"
            )
            
            # Update resolution label
            width, height = self.editor.current_image.size
            self.editor.resolution_label.configure(text=f"{width}x{height}")
    
    def resize_image(self):
        """Enhanced resize image tool with professional features."""
        if not self.editor.current_image:
            messagebox.showinfo("Info", "Please open an image first")
            return
        
        # Create a dialog for advanced resize options
        resize_dialog = ctk.CTkToplevel(self.editor.root)
        resize_dialog.title("Resize Image")
        resize_dialog.geometry("500x400")
        resize_dialog.transient(self.editor.root)
        resize_dialog.grab_set()
        
        # Get current image dimensions
        current_width, current_height = self.editor.current_image.size
        
        # Create variables to store new dimensions
        width_var = tk.IntVar(value=current_width)
        height_var = tk.IntVar(value=current_height)
        maintain_aspect_ratio = tk.BooleanVar(value=True)
        resize_method_var = tk.StringVar(value="LANCZOS")
        resize_unit_var = tk.StringVar(value="pixels")
        
        # Calculate aspect ratio
        aspect_ratio = current_width / current_height
        
        # Function to update dimensions based on aspect ratio
        def update_dimensions(source):
            if maintain_aspect_ratio.get():
                if source == "width":
                    new_width = width_var.get()
                    height_var.set(int(new_width / aspect_ratio))
                else:
                    new_height = height_var.get()
                    width_var.set(int(new_height * aspect_ratio))
        
        # Function to handle percentage input
        def apply_percentage():
            try:
                percentage = float(percentage_entry.get())
                if percentage <= 0:
                    messagebox.showerror("Error", "Percentage must be greater than 0")
                    return
                    
                new_width = int(current_width * percentage / 100)
                new_height = int(current_height * percentage / 100)
                
                width_var.set(new_width)
                height_var.set(new_height)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid percentage")
        
        # Function to handle preset sizes
        def apply_preset(preset):
            if preset == "HD (1280x720)":
                if current_width / current_height > 16/9:  # Wider than 16:9
                    width_var.set(1280)
                    update_dimensions("width")
                else:
                    height_var.set(720)
                    update_dimensions("height")
            elif preset == "Full HD (1920x1080)":
                if current_width / current_height > 16/9:
                    width_var.set(1920)
                    update_dimensions("width")
                else:
                    height_var.set(1080)
                    update_dimensions("height")
            elif preset == "4K (3840x2160)":
                if current_width / current_height > 16/9:
                    width_var.set(3840)
                    update_dimensions("width")
                else:
                    height_var.set(2160)
                    update_dimensions("height")
            elif preset == "Square":
                # Take the smaller dimension
                size = min(current_width, current_height)
                width_var.set(size)
                height_var.set(size)
                
        # Create main frame
        main_frame = ctk.CTkFrame(resize_dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Current dimensions display
        current_dim_label = ctk.CTkLabel(
            main_frame, 
            text=f"Current Dimensions: {current_width} × {current_height} pixels",
            font=ctk.CTkFont(weight="bold")
        )
        current_dim_label.pack(pady=(0, 15))
        
        # Create tabs for different resize methods
        tab_view = ctk.CTkTabview(main_frame)
        tab_view.pack(fill="both", expand=True)
        
        # Add tabs
        tab_view.add("Dimensions")
        tab_view.add("Percentage")
        tab_view.add("Presets")
        
        # === DIMENSIONS TAB ===
        dim_tab = tab_view.tab("Dimensions")
        
        # Width input
        width_frame = ctk.CTkFrame(dim_tab)
        width_frame.pack(fill="x", pady=(10, 5))
        
        width_label = ctk.CTkLabel(width_frame, text="Width:", width=60)
        width_label.pack(side="left", padx=(0, 10))
        
        width_entry = ctk.CTkEntry(width_frame, textvariable=width_var, width=80)
        width_entry.pack(side="left")
        width_entry.bind("<FocusOut>", lambda e: update_dimensions("width"))
        width_entry.bind("<Return>", lambda e: update_dimensions("width"))
        
        width_unit = ctk.CTkLabel(width_frame, text="pixels")
        width_unit.pack(side="left", padx=(5, 0))
        
        # Height input
        height_frame = ctk.CTkFrame(dim_tab)
        height_frame.pack(fill="x", pady=5)
        
        height_label = ctk.CTkLabel(height_frame, text="Height:", width=60)
        height_label.pack(side="left", padx=(0, 10))
        
        height_entry = ctk.CTkEntry(height_frame, textvariable=height_var, width=80)
        height_entry.pack(side="left")
        height_entry.bind("<FocusOut>", lambda e: update_dimensions("height"))
        height_entry.bind("<Return>", lambda e: update_dimensions("height"))
        
        height_unit = ctk.CTkLabel(height_frame, text="pixels")
        height_unit.pack(side="left", padx=(5, 0))
        
        # Maintain aspect ratio checkbox
        aspect_checkbox = ctk.CTkCheckBox(
            dim_tab, 
            text="Maintain aspect ratio",
            variable=maintain_aspect_ratio
        )
        aspect_checkbox.pack(anchor="w", pady=10)
        
        # === PERCENTAGE TAB ===
        pct_tab = tab_view.tab("Percentage")
        
        pct_frame = ctk.CTkFrame(pct_tab)
        pct_frame.pack(fill="x", pady=(20, 10))
        
        pct_label = ctk.CTkLabel(pct_frame, text="Scale by:")
        pct_label.pack(side="left", padx=(0, 10))
        
        percentage_entry = ctk.CTkEntry(pct_frame, width=80)
        percentage_entry.insert(0, "100")
        percentage_entry.pack(side="left")
        
        pct_symbol = ctk.CTkLabel(pct_frame, text="%")
        pct_symbol.pack(side="left", padx=(5, 10))
        
        apply_pct_btn = ctk.CTkButton(
            pct_frame,
            text="Apply",
            command=apply_percentage
        )
        apply_pct_btn.pack(side="left", padx=(10, 0))
        
        # Common percentage buttons
        common_pct_frame = ctk.CTkFrame(pct_tab)
        common_pct_frame.pack(fill="x", pady=10)
        
        common_pct_label = ctk.CTkLabel(common_pct_frame, text="Common scales:")
        common_pct_label.pack(anchor="w", pady=(0, 5))
        
        pct_buttons_frame = ctk.CTkFrame(common_pct_frame)
        pct_buttons_frame.pack(fill="x")
        
        for pct in [25, 50, 75, 100, 150, 200]:
            pct_btn = ctk.CTkButton(
                pct_buttons_frame,
                text=f"{pct}%",
                width=60,
                command=lambda p=pct: [percentage_entry.delete(0, "end"), 
                                    percentage_entry.insert(0, str(p)), 
                                    apply_percentage()]
            )
            pct_btn.pack(side="left", padx=5, pady=5)
        
        # === PRESETS TAB ===
        preset_tab = tab_view.tab("Presets")
        
        preset_label = ctk.CTkLabel(preset_tab, text="Common image sizes:")
        preset_label.pack(anchor="w", pady=(10, 5))
        
        presets = [
            "HD (1280x720)", 
            "Full HD (1920x1080)", 
            "4K (3840x2160)",
            "Square"
        ]
        
        for preset in presets:
            preset_btn = ctk.CTkButton(
                preset_tab,
                text=preset,
                command=lambda p=preset: apply_preset(p)
            )
            preset_btn.pack(fill="x", pady=5)
        
        # Advanced options frame
        advanced_frame = ctk.CTkFrame(main_frame)
        advanced_frame.pack(fill="x", pady=(15, 0))
        
        advanced_label = ctk.CTkLabel(
            advanced_frame, 
            text="Advanced Options",
            font=ctk.CTkFont(weight="bold")
        )
        advanced_label.pack(anchor="w", pady=(5, 10))
        
        # Resampling method
        method_frame = ctk.CTkFrame(advanced_frame)
        method_frame.pack(fill="x", pady=5)
        
        method_label = ctk.CTkLabel(method_frame, text="Resampling method:")
        method_label.pack(side="left", padx=(0, 10))
        
        methods = {
            "NEAREST": "Nearest (Fastest, lowest quality)",
            "BOX": "Box (Fast, pixelated)",
            "BILINEAR": "Bilinear (Good balance)",
            "HAMMING": "Hamming (Good for downscaling)",
            "BICUBIC": "Bicubic (Better quality)",
            "LANCZOS": "Lanczos (Best quality, slowest)"
        }
        
        method_dropdown = ctk.CTkOptionMenu(
            method_frame,
            values=list(methods.values()),
            variable=resize_method_var
        )
        method_dropdown.set(methods["LANCZOS"])
        method_dropdown.pack(side="left", fill="x", expand=True)
        
        # Preview option
        preview_frame = ctk.CTkFrame(main_frame)
        preview_frame.pack(fill="x", pady=(15, 0))
        
        preview_var = tk.BooleanVar(value=False)
        preview_checkbox = ctk.CTkCheckBox(
            preview_frame,
            text="Show preview (may be slow for large images)",
            variable=preview_var
        )
        preview_checkbox.pack(anchor="w")
        
        # Preview canvas
        preview_canvas_frame = ctk.CTkFrame(main_frame)
        preview_canvas_frame.pack(fill="both", expand=True, pady=(10, 0))
        preview_canvas_frame.pack_forget()  # Initially hidden
        
        preview_canvas = tk.Canvas(
            preview_canvas_frame,
            bg="#2a2d2e",
            highlightthickness=0
        )
        preview_canvas.pack(fill="both", expand=True)
        
        # Function to update preview
        def update_preview():
            if not preview_var.get() or not self.editor.current_image:
                preview_canvas_frame.pack_forget()
                return
                
            # Show preview frame
            preview_canvas_frame.pack(fill="both", expand=True, pady=(10, 0))
            
            # Get selected resampling method
            method_name = list(methods.keys())[list(methods.values()).index(resize_method_var.get())]
            resampling_method = getattr(Image, method_name)
            
            # Create preview image
            try:
                preview_img = self.editor.current_image.copy()
                preview_img.thumbnail((300, 300))  # Limit preview size
                
                # Apply resize with current settings
                new_width = width_var.get()
                new_height = height_var.get()
                
                # Calculate preview dimensions (maintaining the new aspect ratio)
                preview_ratio = new_width / new_height
                if preview_ratio > 1:
                    preview_width = 300
                    preview_height = int(300 / preview_ratio)
                else:
                    preview_height = 300
                    preview_width = int(300 * preview_ratio)
                    
                preview_img = preview_img.resize((preview_width, preview_height), resampling_method)
                
                # Display preview
                preview_photo = ImageTk.PhotoImage(preview_img)
                preview_canvas.delete("all")
                preview_canvas.create_image(
                    preview_canvas.winfo_width()//2,
                    preview_canvas.winfo_height()//2,
                    image=preview_photo,
                    anchor="center"
                )
                # Keep a reference to prevent garbage collection
                preview_canvas.image = preview_photo
                
            except Exception as e:
                messagebox.showerror("Preview Error", f"Could not generate preview: {str(e)}")
                preview_var.set(False)
                preview_canvas_frame.pack_forget()
        
        # Connect preview checkbox to update function
        preview_var.trace_add("write", lambda *args: update_preview())
        
        # Connect dimension changes to preview update
        width_var.trace_add("write", lambda *args: update_preview() if preview_var.get() else None)
        height_var.trace_add("write", lambda *args: update_preview() if preview_var.get() else None)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=(15, 0))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=resize_dialog.destroy
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        apply_btn = ctk.CTkButton(
            buttons_frame,
            text="Apply",
            command=lambda: self.apply_resize(
                width_var.get(), 
                height_var.get(), 
                list(methods.keys())[list(methods.values()).index(resize_method_var.get())],
                resize_dialog
            )
        )
        apply_btn.pack(side="right")
        
        # Center the dialog on the screen
        resize_dialog.update_idletasks()
        width = resize_dialog.winfo_width()
        height = resize_dialog.winfo_height()
        x = (resize_dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (resize_dialog.winfo_screenheight() // 2) - (height // 2)
        resize_dialog.geometry(f"{width}x{height}+{x}+{y}")

    def apply_resize(self, new_width, new_height, method_name, dialog):
        """Apply the resize operation with the selected parameters."""
        if not self.editor.current_image:
            messagebox.showerror("Error", "No image to resize")
            dialog.destroy()
            return
        
        try:
            # Validate dimensions
            if new_width <= 0 or new_height <= 0:
                messagebox.showerror("Error", "Width and height must be greater than 0")
                return
                
            # Get the resampling method from PIL
            resampling_method = getattr(Image, method_name)
            
            # Add current state to history before making changes
            self.editor.push_to_history()
            
            # Perform the resize operation
            self.editor.current_image = self.editor.current_image.resize(
                (new_width, new_height), 
                resampling_method
            )
            
            # Update the display
            self.display_image_on_canvas()
            
            # Update status bar
            self.editor.status_bar.configure(text=f"Image resized to {new_width}x{new_height} using {method_name}")
            
            # Close the dialog
            dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Resize Error", f"Could not resize image: {str(e)}")

    def rotate_image(self, angle):
        if not self.editor.current_image:
            messagebox.showinfo("Info", "Please open an image first")
            return
        
        try:
            # Add current state to history before making changes
            self.editor.push_to_history()
            
            # Rotate the image (expand=True to show the entire rotated image)
            self.editor.current_image = self.editor.current_image.rotate(angle, expand=True, resample=Image.BICUBIC)
            self.display_image_on_canvas()
            self.editor.status_bar.configure(text=f"Image rotated by {angle} degrees")
        except Exception as e:
            messagebox.showerror("Error", f"Could not rotate image: {str(e)}")
    
    def flip_horizontal(self):
        if not self.editor.current_image:
            messagebox.showinfo("Info", "Please open an image first")
            return
        
        # Add current state to history before making changes
        self.editor.push_to_history()
        
        self.editor.current_image = ImageOps.mirror(self.editor.current_image)
        self.display_image_on_canvas()
        self.editor.status_bar.configure(text="Image flipped horizontally")
    
    def flip_vertical(self):
        if not self.editor.current_image:
            messagebox.showinfo("Info", "Please open an image first")
            return
        
        # Add current state to history before making changes
        self.editor.push_to_history()
        
        self.editor.current_image = ImageOps.flip(self.editor.current_image)
        self.display_image_on_canvas()
        self.editor.status_bar.configure(text="Image flipped vertically")
    
    def reset_image(self):
        if self.editor.original_image:
            # Add current state to history before making changes
            self.editor.push_to_history()
            
            self.editor.current_image = self.editor.original_image.copy()
            self.display_image_on_canvas()
            self.editor.status_bar.configure(text="Image reset to original")
# Filter functions
    def apply_brightness(self, value):
        """Apply brightness adjustment to the image."""
        if not self.editor.current_image or not self.editor.original_image:
            return
        
        self.brightness_value = value
        
        # Apply the filter
        self._apply_combined_adjustments()
    
    def apply_contrast(self, value):
        """Apply contrast adjustment to the image."""
        if not self.editor.current_image or not self.editor.original_image:
            return
        
        self.contrast_value = value
        
        # Apply the filter
        self._apply_combined_adjustments()
    
    def apply_saturation(self, value):
        """Apply saturation adjustment to the image."""
        if not self.editor.current_image or not self.editor.original_image:
            return
        
        self.saturation_value = value
        
        # Apply the filter
        self._apply_combined_adjustments()
    
    def _apply_combined_adjustments(self):
        """Apply all adjustments at once to avoid quality loss from multiple operations."""
        if not self.editor.current_image or not self.editor.original_image:
            return
        
        # Start with the original image
        img = self.editor.original_image.copy()
        
        # Apply brightness (convert slider value to enhancement factor)
        if self.brightness_value != 0:
            factor = 1.0 + (self.brightness_value / 100.0)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(factor)
        
        # Apply contrast
        if self.contrast_value != 0:
            factor = 1.0 + (self.contrast_value / 100.0)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(factor)
        
        # Apply saturation
        if self.saturation_value != 0:
            factor = 1.0 + (self.saturation_value / 100.0)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(factor)
        
        # Update the current image
        self.editor.current_image = img
        
        # Display the updated image
        self.display_image_on_canvas()
    
    def apply_grayscale(self):
        """Convert the image to grayscale."""
        if not self.editor.current_image:
            messagebox.showinfo("Info", "Please open an image first")
            return
        
        # Add current state to history before making changes
        self.editor.push_to_history()
        
        # Convert to grayscale
        self.editor.current_image = ImageOps.grayscale(self.editor.current_image).convert('RGB')
        
        # Display the updated image
        self.display_image_on_canvas()
        
        # Update status
        self.editor.status_bar.configure(text="Grayscale filter applied")
        
        # Reset adjustment sliders
        self.brightness_value = 0
        self.contrast_value = 0
        self.saturation_value = 0
        
        # Update UI sliders if they exist
        if hasattr(self.editor, 'sidebar_ui'):
            self.editor.sidebar_ui.brightness_slider.set(0)
            self.editor.sidebar_ui.contrast_slider.set(0)
            self.editor.sidebar_ui.saturation_slider.set(0)
    
    def apply_blur(self):
        """Apply blur filter to the image."""
        if not self.editor.current_image:
            messagebox.showinfo("Info", "Please open an image first")
            return
        
        # Add current state to history before making changes
        self.editor.push_to_history()
        
        # Apply blur filter
        self.editor.current_image = self.editor.current_image.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Display the updated image
        self.display_image_on_canvas()
        
        # Update status
        self.editor.status_bar.configure(text="Blur filter applied")
    
    def apply_sharpen(self):
        """Apply sharpen filter to the image."""
        if not self.editor.current_image:
            messagebox.showinfo("Info", "Please open an image first")
            return
        
        # Add current state to history before making changes
        self.editor.push_to_history()
        
        # Apply sharpen filter
        self.editor.current_image = self.editor.current_image.filter(ImageFilter.SHARPEN)
        
        # Display the updated image
        self.display_image_on_canvas()
        
        # Update status
        self.editor.status_bar.configure(text="Sharpen filter applied")
    
    def apply_edge_detection(self):
        """Apply edge detection filter to the image."""
        if not self.editor.current_image:
            messagebox.showinfo("Info", "Please open an image first")
            return
        
        # Add current state to history before making changes
        self.editor.push_to_history()
        
        # Apply edge detection filter
        self.editor.current_image = self.editor.current_image.filter(ImageFilter.FIND_EDGES)
        
        # Display the updated image
        self.display_image_on_canvas()
        
        # Update status
        self.editor.status_bar.configure(text="Edge detection filter applied")
    
    def apply_emboss(self):
        """Apply emboss filter to the image."""
        if not self.editor.current_image:
            messagebox.showinfo("Info", "Please open an image first")
            return
        
        # Add current state to history before making changes
        self.editor.push_to_history()
        
        # Apply emboss filter
        self.editor.current_image = self.editor.current_image.filter(ImageFilter.EMBOSS)
        
        # Display the updated image
        self.display_image_on_canvas()
        
        # Update status
        self.editor.status_bar.configure(text="Emboss filter applied")
    
    def apply_sepia(self):
        """Apply sepia tone filter to the image."""
        if not self.editor.current_image:
            messagebox.showinfo("Info", "Please open an image first")
            return
        
        # Add current state to history before making changes
        self.editor.push_to_history()
        
        # Convert to grayscale first
        grayscale = ImageOps.grayscale(self.editor.current_image)
        
        # Apply sepia tone (using a simple method)
        width, height = grayscale.size
        sepia = Image.new('RGB', (width, height))
        
        # Create sepia tone by adjusting RGB values
        for x in range(width):
            for y in range(height):
                gray_value = grayscale.getpixel((x, y))
                r = min(int(gray_value * 1.2), 255)
                g = min(int(gray_value * 0.95), 255)
                b = int(gray_value * 0.7)
                sepia.putpixel((x, y), (r, g, b))
        
        self.editor.current_image = sepia
        
        # Display the updated image
        self.display_image_on_canvas()
        
        # Update status
        self.editor.status_bar.configure(text="Sepia filter applied")
    
    def apply_negative(self):
        """Apply negative/invert filter to the image."""
        if not self.editor.current_image:
            messagebox.showinfo("Info", "Please open an image first")
            return
        
        # Add current state to history before making changes
        self.editor.push_to_history()
        
        # Invert the image
        self.editor.current_image = ImageOps.invert(self.editor.current_image)
        
        # Display the updated image
        self.display_image_on_canvas()
        
        # Update status
        self.editor.status_bar.configure(text="Negative filter applied")