import os
from cairosvg import svg2png
import requests
import io

# Create directory for icons
icons_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons")
os.makedirs(icons_dir, exist_ok=True)

# FontAwesome free icons URLs (you can replace these with actual URLs or local paths)
icon_urls = {
    "pencil": "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/solid/pencil.svg",
    "brush": "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/solid/paint-brush.svg",
    "eraser": "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/solid/eraser.svg",
    "text": "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/solid/font.svg",
    "draw": "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/solid/pen.svg",
    "grayscale": "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/solid/adjust.svg",
    "reset": "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/master/svgs/solid/undo.svg",
}

# Download and convert SVG icons to PNG
for name, url in icon_urls.items():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            output_path = os.path.join(icons_dir, f"{name}.png")
            svg2png(bytestring=response.content, write_to=output_path, output_width=64, output_height=64)
            print(f"Generated {name}.png")
        else:
            print(f"Failed to download {name} icon: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error processing {name} icon: {e}")

print("Icon generation complete!")
