from PIL import Image
from .layer import Layer

class LayerManager:
    def __init__(self, editor):
        self.editor = editor
        self.layers = []  # The layer stack (bottom to top)
        self.active_layer_index = -1  # Index of the currently selected layer
        self.canvas_size = (800, 600)  # Default size
        
    def create_new_document(self, width, height, bg_color="white"):
        """Create a new document with a background layer"""
        self.canvas_size = (width, height)
        self.layers = []
        
        # Create background layer
        bg_image = Image.new("RGB", (width, height), bg_color)
        bg_layer = Layer(bg_image, name="Background")
        self.add_layer(bg_layer)
        
    def add_layer(self, layer=None):
        """Add a new layer to the stack"""
        if layer is None:
            # Create a transparent layer
            transparent = Image.new("RGBA", self.canvas_size, (0, 0, 0, 0))
            layer = Layer(transparent, name=f"Layer {len(self.layers) + 1}")
            
        self.layers.append(layer)
        self.active_layer_index = len(self.layers) - 1
        self.update_layer_ui()
        return layer
        
    def delete_layer(self, index=None):
        """Delete a layer from the stack"""
        if index is None:
            index = self.active_layer_index
            
        if index < 0 or index >= len(self.layers) or len(self.layers) <= 1:
            # Don't delete if it's invalid or the last layer
            return False
            
        del self.layers[index]
        
        # Update active layer index
        if self.active_layer_index >= len(self.layers):
            self.active_layer_index = len(self.layers) - 1
            
        self.update_layer_ui()
        return True
        
    def move_layer(self, from_index, to_index):
        """Move a layer to a new position in the stack"""
        if from_index < 0 or from_index >= len(self.layers) or \
           to_index < 0 or to_index >= len(self.layers):
            return False
            
        layer = self.layers.pop(from_index)
        self.layers.insert(to_index, layer)
        
        # Update active layer if needed
        if self.active_layer_index == from_index:
            self.active_layer_index = to_index
            
        self.update_layer_ui()
        return True
        
    def duplicate_layer(self, index=None):
        """Duplicate a layer"""
        if index is None:
            index = self.active_layer_index
            
        if index < 0 or index >= len(self.layers):
            return None
            
        source_layer = self.layers[index]
        
        # Create a copy of the layer
        new_image = source_layer.image.copy() if source_layer.image else None
        new_layer = Layer(
            new_image,
            name=f"Copy of {source_layer.name}",
            visible=source_layer.visible,
            opacity=source_layer.opacity,
            blend_mode=source_layer.blend_mode
        )
        
        # Insert after the source layer
        self.layers.insert(index + 1, new_layer)
        self.active_layer_index = index + 1
        self.update_layer_ui()
        return new_layer
        
    def merge_layers(self, index1, index2):
        """Merge two layers together"""
        if index1 < 0 or index1 >= len(self.layers) or \
           index2 < 0 or index2 >= len(self.layers):
            return False
            
        # Ensure index1 is below index2
        if index1 > index2:
            index1, index2 = index2, index1
            
        bottom_layer = self.layers[index1]
        top_layer = self.layers[index2]
        
        # Create a new image for the merged result
        if bottom_layer.image.mode != 'RGBA':
            merged_image = bottom_layer.image.convert('RGBA')
        else:
            merged_image = bottom_layer.image.copy()
            
        # Apply the top layer with its opacity
        if top_layer.visible and top_layer.image:
            top_image = top_layer.apply_opacity()
            if top_image:
                # Composite the images
                merged_image.paste(top_image, (top_layer.x_offset, top_layer.y_offset), top_image)
                
        # Create a new layer with the merged result
        merged_layer = Layer(
            merged_image,
            name=f"Merged Layer",
            visible=True,
            opacity=100,
            blend_mode="Normal"
        )
        
        # Replace the bottom layer with the merged layer
        self.layers[index1] = merged_layer
        
        # Remove the top layer
        del self.layers[index2]
        
        # Update active layer index
        if self.active_layer_index == index2:
            self.active_layer_index = index1
        elif self.active_layer_index > index2:
            self.active_layer_index -= 1
            
        self.update_layer_ui()
        return True
        
    def flatten_image(self):
        """Flatten all visible layers into a single layer"""
        if not self.layers:
            return None
            
        # Start with a blank image
        flattened = Image.new("RGBA", self.canvas_size, (0, 0, 0, 0))
        
        # Composite all visible layers
        for layer in self.layers:
            if layer.visible and layer.image:
                layer_image = layer.apply_opacity()
                if layer_image:
                    flattened.paste(layer_image, (layer.x_offset, layer.y_offset), layer_image)
                    
        # Create a new background layer
        bg_layer = Layer(flattened.convert("RGB"), name="Flattened Image")
        
        # Replace all layers with the flattened layer
        self.layers = [bg_layer]
        self.active_layer_index = 0
        self.update_layer_ui()
        
        return flattened
        
    def get_composite_image(self):
        """Get a composite of all visible layers for display"""
        if not self.layers:
            return None
            
        # Start with a blank image
        composite = Image.new("RGBA", self.canvas_size, (0, 0, 0, 0))
        
        # Composite all visible layers
        for layer in self.layers:
            if layer.visible and layer.image:
                layer_image = layer.apply_opacity()
                if layer_image:
                    composite.paste(layer_image, (layer.x_offset, layer.y_offset), layer_image)
                    
        return composite
        
    def update_layer_ui(self):
        """Update the layer panel UI"""
        # This will be implemented to update the layer panel
        if hasattr(self.editor, 'layer_panel'):
            self.editor.layer_panel.update_layers()
            
        # Update the canvas with the composite image
        composite = self.get_composite_image()
        if composite and hasattr(self.editor, 'display_image_on_canvas'):
            self.editor.current_image = composite
            self.editor.display_image_on_canvas()

    def clear_layers(self):
        """Remove all layers from the layer manager"""
        # Store the current canvas size before clearing
        canvas_size = self.canvas_size
        
        # Clear the layers list
        self.layers = []
        
        # Reset the active layer index
        self.active_layer_index = -1
        
        # Maintain the canvas size
        self.canvas_size = canvas_size
        
        # Update the layer panel if it exists
        if hasattr(self, 'layer_panel') and self.layer_panel is not None:
            self.layer_panel.update_layer_list()
            
