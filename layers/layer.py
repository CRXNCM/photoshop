from PIL import Image

class Layer:
    def __init__(self, image=None, name="New Layer", visible=True, opacity=100, blend_mode="Normal"):
        # The actual image data (PIL Image)
        self.image = image
        # Layer properties
        self.name = name
        self.visible = visible
        self.opacity = opacity  # 0-100
        self.blend_mode = blend_mode
        # Layer position (for transformations)
        self.x_offset = 0
        self.y_offset = 0
        # Layer mask (optional)
        self.mask = None
        
    def resize(self, width, height):
        """Resize the layer's image"""
        if self.image:
            self.image = self.image.resize((width, height), Image.LANCZOS)
            
    def apply_opacity(self):
        """Apply the opacity setting to create a display version of the image"""
        if not self.image or self.opacity == 100:
            return self.image
            
        # Create a copy with alpha channel
        if self.image.mode != 'RGBA':
            img_with_alpha = self.image.convert('RGBA')
        else:
            img_with_alpha = self.image.copy()
            
        # Apply opacity
        alpha_factor = self.opacity / 100
        data = list(img_with_alpha.getdata())
        new_data = [(r, g, b, int(a * alpha_factor)) for r, g, b, a in data]
        img_with_alpha.putdata(new_data)
        
        return img_with_alpha
