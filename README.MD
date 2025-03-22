# 🎨 Modern Image Editor

A professional, feature-rich image editing application built with Python and CustomTkinter, offering a modern UI experience with powerful editing capabilities.

![Modern Image Editor](https://via.placeholder.com/800x450?text=Modern+Image+Editor)

## 🚀 Features

### 🖥️ User Interface

- **🎨 Modern Design**: Clean, intuitive interface with dark and light mode support
- **🔧 Customizable Layout**: Toolbar, sidebar, and properties panel for efficient workflow
- **📂 Drag and Drop**: Easily open images by dragging them into the application
- **⌨️ Keyboard Shortcuts**: Boost productivity with comprehensive keyboard shortcuts

### ✂️ Core Editing Features

- **📁 Basic Operations**: Open, save, resize, and reset images
- **🔄 Transformations**: Rotate, flip horizontal, flip vertical
- **📐 Cropping**: Interactive crop tool with visual selection
- **📝 Text Tool**: Add customizable text with font selection, size, color, and styling options
- **🔍 Zoom Controls**: Zoom in/out with mouse wheel or keyboard shortcuts

### 🎛️ Image Adjustments

- **🌈 Color Manipulation**: Brightness, contrast, and saturation controls
- **🎭 Filters**: Grayscale, blur, sharpen, edge detection, emboss, sepia, and negative
- **🔬 Advanced Editing**: Professional-grade image processing capabilities

### 🔄 History Management

- **⏪ Undo/Redo**: Full history tracking for all operations
- **🛡️ Non-destructive Editing**: Original image preserved throughout editing process

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/CRXNCM/photoshop.git

# Navigate to the project directory
cd modern-image-editor

# Install dependencies
pip install -r requirements.txt

# Run the application
python image_editor.py
```

📌 Requirements

🐍 Python 3.7+

🖼️ Pillow (PIL Fork)

🎨 CustomTkinter

📂 tkinterdnd2 (optional, for drag and drop support)

⌨️ Keyboard Shortcuts

Shortcut

Action

Ctrl+O

🖼️ Open Image

Ctrl+S

💾 Save Image

Ctrl+Z

↩️ Undo

Ctrl+Y

↪️ Redo

Ctrl+R

🔄 Reset Image

Ctrl++

🔍 Zoom In

Ctrl+-

🔎 Zoom Out

Esc

❌ Cancel Text Editing

Ctrl+Enter

✅ Confirm Text

### 📂 Project Structure
```bash
modern-image-editor/
├── image_editor.py       # 🎯 Main application file
├── ui/                   # 🎨 User interface components
│   ├── toolbar.py        # 🛠️ Top toolbar implementation
│   ├── sidebar.py        # 📂 Left sidebar with tools
│   ├── menu_manager.py   # 📜 Application menu system
│   └── properties_panel.py # ⚙️ Right panel for tool properties
├── tools/                # 🖼️ Image editing tools
│   └── tools.py          # ✂️ Core editing functionality
└── utils/                # 🏗️ Utility modules
    └── keyboard_shortcuts.py # ⌨️ Keyboard shortcut handling

```
🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add some amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

🙌 Acknowledgments

🎨 CustomTkinter for the modern UI components

🖼️ Pillow for image processing capabilities

🌟 All contributors who have helped improve this project

Modern Image Editor - Professional image editing made simple 🚀