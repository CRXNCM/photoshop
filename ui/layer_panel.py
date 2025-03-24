import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import os

class LayerPanel:
    def __init__(self, editor, parent_frame):
        self.editor = editor
        self.parent_frame = parent_frame
        self.layer_frames = []  # Store references to layer UI elements
        
        self.create_layer_panel()
        
    def create_layer_panel(self):
        """Create the layer panel UI"""
        # Main frame for the layer panel
        self.panel_frame = ctk.CTkFrame(self.parent_frame)
        self.panel_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with title and buttons
        header_frame = ctk.CTkFrame(self.panel_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Layers", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Layer operation buttons
        buttons_frame = ctk.CTkFrame(header_frame)
        buttons_frame.pack(side=tk.RIGHT)
        
        # Add layer button
        add_btn = ctk.CTkButton(
            buttons_frame,
            text="+",
            width=30,
            height=30,
            command=self.add_new_layer
        )
        add_btn.pack(side=tk.LEFT, padx=2)
        
        # Delete layer button
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="-",
            width=30,
            height=30,
            command=self.delete_active_layer
        )
        delete_btn.pack(side=tk.LEFT, padx=2)
        
        # Duplicate layer button
        duplicate_btn = ctk.CTkButton(
            buttons_frame,
            text="D",
            width=30,
            height=30,
            command=self.duplicate_active_layer
        )
        duplicate_btn.pack(side=tk.LEFT, padx=2)
        
        # Merge layers button
        merge_btn = ctk.CTkButton(
            buttons_frame,
            text="M",
            width=30,
            height=30,
            command=self.merge_with_below
        )
        merge_btn.pack(side=tk.LEFT, padx=2)
        
        # Scrollable frame for layers
        self.layers_container = ctk.CTkScrollableFrame(self.panel_frame)
        self.layers_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Opacity and blend mode controls
        controls_frame = ctk.CTkFrame(self.panel_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Opacity control
        opacity_label = ctk.CTkLabel(controls_frame, text="Opacity:")
        opacity_label.pack(anchor="w", padx=5, pady=(5, 0))
        
        self.opacity_var = tk.IntVar(value=100)
        self.opacity_slider = ctk.CTkSlider(
            controls_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            variable=self.opacity_var,
            command=self.change_layer_opacity
        )
        self.opacity_slider.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Blend mode control
        blend_label = ctk.CTkLabel(controls_frame, text="Blend Mode:")
        blend_label.pack(anchor="w", padx=5, pady=(5, 0))
        
        self.blend_var = tk.StringVar(value="Normal")
        blend_modes = ["Normal", "Multiply", "Screen", "Overlay", "Soft Light", "Hard Light", "Difference"]
        self.blend_dropdown = ctk.CTkOptionMenu(
            controls_frame,
            values=blend_modes,
            variable=self.blend_var,
            command=self.change_blend_mode
        )
        self.blend_dropdown.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Update the layer list
        self.update_layers()
        
    def update_layers(self):
        """Update the layer list UI"""
        # Clear existing layer frames
        for frame in self.layer_frames:
            frame.destroy()
        self.layer_frames = []
        
        # No layers to display
        if not hasattr(self.editor, 'layer_manager') or not self.editor.layer_manager.layers:
            return
            
        # Create a frame for each layer (in reverse order - top to bottom)
        for i, layer in enumerate(reversed(self.editor.layer_manager.layers)):
            layer_index = len(self.editor.layer_manager.layers) - 1 - i
            layer_frame = self.create_layer_item(layer, layer_index)
            self.layer_frames.append(layer_frame)
            
        # Update opacity slider and blend mode dropdown for active layer
        self.update_layer_controls()
            
    def create_layer_item(self, layer, index):
        """Create a UI item for a single layer"""
        # Frame for the layer
        layer_frame = ctk.CTkFrame(self.layers_container)
        layer_frame.pack(fill=tk.X, padx=2, pady=2)
        
        # Make the frame clickable to select the layer
        layer_frame.bind("<Button-1>", lambda e, idx=index: self.select_layer(idx))
        
        # Highlight active layer
        if index == self.editor.layer_manager.active_layer_index:
            layer_frame.configure(border_width=2, border_color=("blue", "#1F6AA5"))
        
        # Visibility toggle
        visible_var = tk.BooleanVar(value=layer.visible)
        visible_cb = ctk.CTkCheckBox(
            layer_frame,
            text="",
            variable=visible_var,
            command=lambda: self.toggle_layer_visibility(index, visible_var.get()),
            width=20,
            height=20
        )
        visible_cb.pack(side=tk.LEFT, padx=5)
        
        # Layer thumbnail (small preview of the layer)
        thumbnail_size = (30, 30)
        if layer.image:
            # Create thumbnail from layer image
            thumb = layer.image.copy()
            thumb.thumbnail(thumbnail_size)
            if thumb.mode == 'RGBA':
                # Create a checkerboard background for transparent images
                bg = self.create_transparency_checkerboard(thumbnail_size)
                bg.paste(thumb, (0, 0), thumb)
                thumb = bg
            tk_thumb = ImageTk.PhotoImage(thumb)
        else:
            # Create empty thumbnail
            thumb = self.create_transparency_checkerboard(thumbnail_size)
            tk_thumb = ImageTk.PhotoImage(thumb)
            
        thumb_label = tk.Label(layer_frame, image=tk_thumb, bg="#2a2d2e", bd=0)
        thumb_label.image = tk_thumb  # Keep a reference
        thumb_label.pack(side=tk.LEFT, padx=5)
        thumb_label.bind("<Button-1>", lambda e, idx=index: self.select_layer(idx))
        
        # Layer name (editable)
        name_var = tk.StringVar(value=layer.name)
        name_entry = ctk.CTkEntry(
            layer_frame,
            textvariable=name_var,
            width=120
        )
        name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        name_entry.bind("<FocusOut>", lambda e, idx=index: self.rename_layer(idx, name_var.get()))
        name_entry.bind("<Return>", lambda e, idx=index: self.rename_layer(idx, name_var.get()))
        
        return layer_frame
    
    def create_transparency_checkerboard(self, size):
        """Create a checkerboard pattern for transparent backgrounds"""
        checker_size = 5  # Size of each checker square
        img = Image.new('RGB', size, color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw the checkerboard pattern
        for y in range(0, size[1], checker_size):
            for x in range(0, size[0], checker_size):
                if (x // checker_size + y // checker_size) % 2 == 0:
                    draw.rectangle(
                        [x, y, x + checker_size - 1, y + checker_size - 1],
                        fill='#cccccc'
                    )
        
        return img
    
    def select_layer(self, index):
        """Select a layer as the active layer"""
        if not hasattr(self.editor, 'layer_manager'):
            return
            
        if 0 <= index < len(self.editor.layer_manager.layers):
            self.editor.layer_manager.active_layer_index = index
            self.update_layers()
            self.update_layer_controls()
    
    def toggle_layer_visibility(self, index, visible):
        """Toggle the visibility of a layer"""
        if not hasattr(self.editor, 'layer_manager'):
            return
            
        if 0 <= index < len(self.editor.layer_manager.layers):
            self.editor.layer_manager.layers[index].visible = visible
            self.editor.layer_manager.update_composite()
    
    def rename_layer(self, index, new_name):
        """Rename a layer"""
        if not hasattr(self.editor, 'layer_manager'):
            return
            
        if 0 <= index < len(self.editor.layer_manager.layers):
            self.editor.layer_manager.layers[index].name = new_name
            self.update_layers()
    
    def add_new_layer(self):
        """Add a new layer"""
        if not hasattr(self.editor, 'layer_manager'):
            return
            
        self.editor.layer_manager.add_layer()
    
    def delete_active_layer(self):
        """Delete the active layer"""
        if not hasattr(self.editor, 'layer_manager'):
            return
            
        self.editor.layer_manager.delete_layer()
    
    def duplicate_active_layer(self):
        """Duplicate the active layer"""
        if not hasattr(self.editor, 'layer_manager'):
            return
            
        self.editor.layer_manager.duplicate_layer()
    
    def merge_with_below(self):
        """Merge the active layer with the layer below it"""
        if not hasattr(self.editor, 'layer_manager'):
            return
            
        active_index = self.editor.layer_manager.active_layer_index
        if active_index > 0:
            self.editor.layer_manager.merge_layers(active_index - 1, active_index)
    
    def change_layer_opacity(self, value=None):
        """Change the opacity of the active layer"""
        if not hasattr(self.editor, 'layer_manager'):
            return
            
        active_index = self.editor.layer_manager.active_layer_index
        if active_index >= 0 and active_index < len(self.editor.layer_manager.layers):
            # Get the value from the slider if not provided
            if value is None:
                value = self.opacity_var.get()
                
            # Update the layer opacity
            self.editor.layer_manager.layers[active_index].opacity = int(value)
            self.editor.layer_manager.update_composite()
    
    def change_blend_mode(self, blend_mode):
        """Change the blend mode of the active layer"""
        if not hasattr(self.editor, 'layer_manager'):
            return
            
        active_index = self.editor.layer_manager.active_layer_index
        if active_index >= 0 and active_index < len(self.editor.layer_manager.layers):
            # Update the layer blend mode
            self.editor.layer_manager.layers[active_index].blend_mode = blend_mode
            self.editor.layer_manager.update_composite()
    
    def update_layer_controls(self):
        """Update the layer controls based on the active layer"""
        if not hasattr(self.editor, 'layer_manager'):
            return
            
        active_index = self.editor.layer_manager.active_layer_index
        if active_index >= 0 and active_index < len(self.editor.layer_manager.layers):
            active_layer = self.editor.layer_manager.layers[active_index]
            
            # Update opacity slider
            self.opacity_var.set(active_layer.opacity)
            
            # Update blend mode dropdown
            self.blend_var.set(active_layer.blend_mode)
            
            # Enable controls
            self.opacity_slider.configure(state="normal")
            self.blend_dropdown.configure(state="normal")
        else:
            # Disable controls if no active layer
            self.opacity_slider.configure(state="disabled")
            self.blend_dropdown.configure(state="disabled")
