import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import os
import json

class SettingsManager:
    def __init__(self, editor):
        self.editor = editor
        self.settings_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "config", 
            "settings.json"
        )
        self.load_settings()
    
    def load_settings(self):
        """Load settings from JSON file"""
        # Default settings
        self.settings = {
            "appearance": {
                "theme": "System"
            },
            "performance": {
                "max_history_states": 20,
                "max_image_dimension": 10000,
                "use_multithreading": True
            }
        }
        
        # Create config directory if it doesn't exist
        config_dir = os.path.dirname(self.settings_file)
        os.makedirs(config_dir, exist_ok=True)
        
        # Load settings if file exists
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    
                    # Update default settings with loaded values
                    for category in loaded_settings:
                        if category in self.settings:
                            for key in loaded_settings[category]:
                                if key in self.settings[category]:
                                    self.settings[category][key] = loaded_settings[category][key]
            except Exception as e:
                print(f"Error loading settings: {e}")

    def save_settings(self):
        """Save settings to JSON file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def apply_settings(self):
        """Apply the current settings to the application"""
        # Apply theme setting
        if "appearance" in self.settings:
            self.apply_theme(self.settings["appearance"]["theme"])
        
        # Apply performance settings
        if "performance" in self.settings:
            # Set max history states if the editor has this attribute
            if hasattr(self.editor, "max_history_states"):
                self.editor.max_history_states = self.settings["performance"]["max_history_states"]
            
            # Apply multithreading setting
            # This might require additional implementation in the editor class
            use_threading = self.settings["performance"]["use_multithreading"]
            if hasattr(self.editor, "use_multithreading"):
                self.editor.use_multithreading = use_threading
        
        # Apply measurement settings
        if "measurement" in self.settings:
            # Apply default unit
            if hasattr(self.editor, "default_unit"):
                self.editor.default_unit = self.settings["measurement"]["default_unit"]
            
            # Apply ruler visibility
            if hasattr(self.editor, "show_rulers"):
                self.editor.show_rulers = self.settings["measurement"]["show_rulers"]
                # Update ruler visibility in the UI
                if hasattr(self.editor, "update_ruler_visibility"):
                    self.editor.update_ruler_visibility()
            
            # Apply grid settings
            if hasattr(self.editor, "show_grid"):
                self.editor.show_grid = self.settings["measurement"]["show_grid"]
                self.editor.grid_

    def apply_theme(self, theme_name):
        """Apply the selected theme"""
        if theme_name == "System":
            ctk.set_appearance_mode("system")
        elif theme_name == "Light":
            ctk.set_appearance_mode("light")
        elif theme_name == "Dark":
            ctk.set_appearance_mode("dark")
        elif theme_name == "Blue":
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
        elif theme_name == "Green":
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("green")
    
    def show_settings_dialog(self):
        """Show the settings dialog window with sidebar layout"""
        # Create a new top-level window
        self.settings_window = ctk.CTkToplevel(self.editor.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("800x500")
        self.settings_window.minsize(700, 400)
        self.settings_window.transient(self.editor.root)
        self.settings_window.grab_set()
        
        # Center the window
        self.settings_window.update_idletasks()
        width = self.settings_window.winfo_width()
        height = self.settings_window.winfo_height()
        x = (self.settings_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.settings_window.winfo_screenheight() // 2) - (height // 2)
        self.settings_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create main container frame
        main_container = ctk.CTkFrame(self.settings_window)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create sidebar frame (left side)
        sidebar_frame = ctk.CTkFrame(main_container, width=200)
        sidebar_frame.pack(side="left", fill="y", padx=(0, 10))
        sidebar_frame.pack_propagate(False)  # Prevent the frame from shrinking
        
        # Create content frame (right side)
        self.content_frame = ctk.CTkFrame(main_container)
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Add title to sidebar
        sidebar_title = ctk.CTkLabel(
            sidebar_frame, 
            text="Settings", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        sidebar_title.pack(pady=(20, 30))
        
        # Create category buttons for sidebar
        # Create category buttons for sidebar
        categories = [
            ("Appearance", self.show_appearance_settings),
            ("Performance", self.show_performance_settings),  # Use the actual method
            ("Measurement", self.show_measurement_settings),
            ("File Handling", lambda: self.show_placeholder("File Handling")),
            ("Tools", lambda: self.show_placeholder("Tools")),
            ("Canvas", lambda: self.show_placeholder("Canvas")),
            ("Keyboard Shortcuts", lambda: self.show_placeholder("Keyboard Shortcuts"))
        ]

                
        # Store references to category buttons
        self.category_buttons = []
        
        for category, command in categories:
            btn = ctk.CTkButton(
                sidebar_frame,
                text=category,
                anchor="w",
                height=40,
                corner_radius=0,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                command=command
            )
            btn.pack(fill="x", pady=2)
            self.category_buttons.append((btn, category))
        
        # Add buttons at the bottom of the window
        button_frame = ctk.CTkFrame(self.settings_window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.settings_window.destroy,
            width=100
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # Save button
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save",
            command=self.save_and_apply_settings,
            width=100
        )
        save_btn.pack(side="right")
        
        # Show appearance settings by default
        self.show_appearance_settings()
    
    def set_active_category(self, active_category):
        """Highlight the active category in the sidebar"""
        for btn, category in self.category_buttons:
            if category == active_category:
                btn.configure(
                    fg_color=("gray75", "gray25"),
                    text_color=("gray10", "gray90")
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=("gray10", "gray90")
                )
    
    def clear_content_frame(self):
        """Clear all widgets from the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_performance_settings(self):
        """Show performance settings in the content frame"""
        self.set_active_category("Performance")
        self.clear_content_frame()
    
        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text="Performance Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(anchor="w", pady=(20, 30), padx=20)
    
        # Make sure performance settings exist in our settings dictionary
        if "performance" not in self.settings:
            self.settings["performance"] = {
                "max_history_states": 20,
                "max_image_dimension": 10000,
                "use_multithreading": True
            }
    
        # History states setting
        history_frame = ctk.CTkFrame(self.content_frame)
        history_frame.pack(fill="x", padx=20, pady=10)
    
        history_label = ctk.CTkLabel(
            history_frame, 
            text="Maximum History States:", 
            width=200,
            anchor="w"
        )
        history_label.pack(side="left", padx=(10, 10))
    
        # Create variable for history states
        self.history_var = tk.IntVar(value=self.settings["performance"]["max_history_states"])

        history_options = [5, 10, 20, 50, 100]
        history_dropdown = ctk.CTkOptionMenu(
            history_frame,
            values=[str(x) for x in history_options],
            variable=tk.StringVar(value=str(self.history_var.get())),
            command=lambda x: self.history_var.set(int(x)),
            width=100
        )

        history_dropdown.pack(side="left")
    
        # History states description
        history_desc = ctk.CTkLabel(
            self.content_frame,
            text="Controls how many undo/redo steps are stored. Higher values use more memory.",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray70"),
            wraplength=500,
            justify="left"
        )
        history_desc.pack(anchor="w", padx=30, pady=(0, 15))
    
        # Max image dimension setting
        dimension_frame = ctk.CTkFrame(self.content_frame)
        dimension_frame.pack(fill="x", padx=20, pady=10)
    
        dimension_label = ctk.CTkLabel(
            dimension_frame, 
            text="Maximum Image Dimension:", 
            width=200,
            anchor="w"
        )
        dimension_label.pack(side="left", padx=(10, 10))
    
        # Create variable for max dimension
        self.dimension_var = tk.IntVar(value=self.settings["performance"]["max_image_dimension"])

        dimension_options = [5000, 10000, 15000, 20000, "No Limit"]
        # Convert the current value to string for the dropdown
        current_dim_str = str(self.dimension_var.get())
        if self.dimension_var.get() == 0:
            current_dim_str = "No Limit"

        dimension_dropdown = ctk.CTkOptionMenu(
            dimension_frame,
            values=[str(x) for x in dimension_options],
            variable=tk.StringVar(value=current_dim_str),
            command=lambda x: self.dimension_var.set(0 if x == "No Limit" else int(x)),
            width=100
        )

        dimension_dropdown.pack(side="left")
    
        # Dimension description
        dimension_desc = ctk.CTkLabel(
            self.content_frame,
            text="Limits the maximum width or height of images. Larger images require more memory and processing power.",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray70"),
            wraplength=500,
            justify="left"
        )
        dimension_desc.pack(anchor="w", padx=30, pady=(0, 15))
    
        # Multithreading setting
        threading_frame = ctk.CTkFrame(self.content_frame)
        threading_frame.pack(fill="x", padx=20, pady=10)
    
        threading_label = ctk.CTkLabel(
            threading_frame, 
            text="Use Multithreading:", 
            width=200,
            anchor="w"
        )
        threading_label.pack(side="left", padx=(10, 10))
    
        # Create variable for multithreading
        self.threading_var = tk.BooleanVar(value=self.settings["performance"]["use_multithreading"])
    
        threading_switch = ctk.CTkSwitch(
            threading_frame,
            text="",
            variable=self.threading_var,
            onvalue=True,
            offvalue=False
        )
        threading_switch.pack(side="left")
    
        # Threading description
        threading_desc = ctk.CTkLabel(
            self.content_frame,
            text="Enables multithreading for image processing operations. Improves performance on multi-core processors, but may increase memory usage.",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray70"),
            wraplength=500,
            justify="left"
        )
        threading_desc.pack(anchor="w", padx=30, pady=(0, 15))
    
        # Performance tips section
        tips_frame = ctk.CTkFrame(self.content_frame)
        tips_frame.pack(fill="x", padx=20, pady=(20, 10))
    
        tips_title = ctk.CTkLabel(
            tips_frame,
            text="Performance Tips",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        tips_title.pack(anchor="w", padx=10, pady=10)
    
        tips_text = (
            "• Close other applications when editing large images\n"
            "• Reduce the number of history states for large projects\n"
            "• Use the 'Resize' tool to work with smaller versions of large images\n"
            "• Save your work frequently to prevent data loss"
        )
    
        tips_label = ctk.CTkLabel(
            tips_frame,
            text=tips_text,
            font=ctk.CTkFont(size=12),
            justify="left",
            wraplength=500
        )
        tips_label.pack(anchor="w", padx=10, pady=(0, 10))

    def show_appearance_settings(self):
        """Show appearance settings in the content frame"""
        self.set_active_category("Appearance")
        self.clear_content_frame()
        
        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text="Appearance Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(anchor="w", pady=(20, 30), padx=20)
        
        # Theme selection
        theme_frame = ctk.CTkFrame(self.content_frame)
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        theme_label = ctk.CTkLabel(theme_frame, text="Theme:", width=100)
        theme_label.pack(side="left", padx=(10, 10))
        
        self.theme_var = tk.StringVar(value=self.settings["appearance"]["theme"])
        theme_options = ["System", "Light", "Dark", "Blue", "Green"]
        
        theme_dropdown = ctk.CTkOptionMenu(
            theme_frame,
            values=theme_options,
            variable=self.theme_var,
            width=200
        )
        theme_dropdown.pack(side="left", padx=(0, 10))
        
        # Preview section
        preview_frame = ctk.CTkFrame(self.content_frame)
        preview_frame.pack(fill="x", padx=20, pady=(30, 10))
        
        preview_label = ctk.CTkLabel(
            preview_frame, 
            text="Preview", 
            font=ctk.CTkFont(weight="bold")
        )
        preview_label.pack(anchor="w", pady=(10, 10), padx=10)
        
        # Preview elements - store as class attribute
        self.preview_elements = ctk.CTkFrame(preview_frame)
        self.preview_elements.pack(fill="x", pady=10, padx=10)
        
        preview_button = ctk.CTkButton(self.preview_elements, text="Button")
        preview_button.pack(side="left", padx=5)
        
        preview_entry = ctk.CTkEntry(self.preview_elements, placeholder_text="Entry")
        preview_entry.pack(side="left", padx=5)
        
        preview_switch = ctk.CTkSwitch(self.preview_elements, text="Switch")
        preview_switch.pack(side="left", padx=5)
        
        # Apply button for preview
        apply_preview_btn = ctk.CTkButton(
            preview_frame,
            text="Preview Theme",
            command=lambda: self.preview_theme(self.theme_var.get()),
            width=150
        )
        apply_preview_btn.pack(pady=10)

        
    def show_placeholder(self, category_name):
        """Show a placeholder for settings categories not yet implemented"""
        self.set_active_category(category_name)
        self.clear_content_frame()
        
        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text=f"{category_name} Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(anchor="w", pady=(20, 30), padx=20)
        
        # Placeholder message
        placeholder = ctk.CTkLabel(
            self.content_frame,
            text=f"The {category_name} settings will be implemented in a future update.",
            font=ctk.CTkFont(size=14)
        )
        placeholder.pack(pady=50, padx=20)
        
        # Coming soon label
        coming_soon = ctk.CTkLabel(
            self.content_frame,
            text="Coming Soon!",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("gray50", "gray70")
        )
        coming_soon.pack(pady=10)
    
    def preview_theme(self, theme_name):
        """Preview the selected theme in a new window"""
        # Create a new window for preview
        preview_window = ctk.CTkToplevel(self.settings_window)
        preview_window.title(f"Theme Preview: {theme_name}")
        preview_window.geometry("400x300")
        preview_window.transient(self.settings_window)
        
        # Apply the theme to this window
        if theme_name == "System":
            preview_window.after(100, lambda: ctk.set_appearance_mode("system"))
        elif theme_name == "Light":
            preview_window.after(100, lambda: ctk.set_appearance_mode("light"))
        elif theme_name == "Dark":
            preview_window.after(100, lambda: ctk.set_appearance_mode("dark"))
        elif theme_name == "Blue":
            preview_window.after(100, lambda: [ctk.set_appearance_mode("dark"), ctk.set_default_color_theme("blue")])
        elif theme_name == "Green":
            preview_window.after(100, lambda: [ctk.set_appearance_mode("dark"), ctk.set_default_color_theme("green")])
        
        # Center the window
        preview_window.update_idletasks()
        width = preview_window.winfo_width()
        height = preview_window.winfo_height()
        x = (preview_window.winfo_screenwidth() // 2) - (width // 2)
        y = (preview_window.winfo_screenheight() // 2) - (height // 2)
        preview_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Add a frame to hold preview elements
        frame = ctk.CTkFrame(preview_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add a title
        title = ctk.CTkLabel(
            frame,
            text=f"{theme_name} Theme Preview",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Add various UI elements to showcase the theme
        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(fill="x", pady=10)
        
        # Regular button
        button = ctk.CTkButton(button_frame, text="Button")
        button.pack(side="left", padx=10)
        
        # Disabled button
        disabled_button = ctk.CTkButton(button_frame, text="Disabled", state="disabled")
        disabled_button.pack(side="left", padx=10)
        
        # Entry
        entry = ctk.CTkEntry(frame, placeholder_text="Entry field")
        entry.pack(fill="x", pady=10)
        
        # Checkbox and switch
        checkbox_frame = ctk.CTkFrame(frame)
        checkbox_frame.pack(fill="x", pady=10)
        
        checkbox = ctk.CTkCheckBox(checkbox_frame, text="Checkbox")
        checkbox.pack(side="left", padx=10)
        
        switch = ctk.CTkSwitch(checkbox_frame, text="Switch")
        switch.pack(side="left", padx=10)
        
        # Slider
        slider = ctk.CTkSlider(frame)
        slider.pack(fill="x", pady=10)
        slider.set(0.7)  # Set to some value
        
        # Close button
        close_btn = ctk.CTkButton(
            frame,
            text="Close Preview",
            command=preview_window.destroy
        )
        close_btn.pack(pady=20)

    def save_and_apply_settings(self):
        """Save and apply the current settings"""
        # Check if theme has changed
        theme_changed = False
        if hasattr(self, 'theme_var'):
            theme_changed = self.settings["appearance"]["theme"] != self.theme_var.get()
            # Update appearance settings
            self.settings["appearance"]["theme"] = self.theme_var.get()
        
        # Update performance settings if they exist
        if hasattr(self, 'history_var'):
            self.settings["performance"]["max_history_states"] = self.history_var.get()
        
        if hasattr(self, 'dimension_var'):
            self.settings["performance"]["max_image_dimension"] = self.dimension_var.get()
        
        if hasattr(self, 'threading_var'):
            self.settings["performance"]["use_multithreading"] = self.threading_var.get()
        
        # Update measurement settings if they exist
        if hasattr(self, 'unit_var'):
            self.settings["measurement"]["default_unit"] = self.unit_var.get()
        
        if hasattr(self, 'ruler_var'):
            self.settings["measurement"]["show_rulers"] = self.ruler_var.get()
        
        if hasattr(self, 'grid_show_var'):
            self.settings["measurement"]["show_grid"] = self.grid_show_var.get()
        
        if hasattr(self, 'grid_size_var'):
            self.settings["measurement"]["grid_size"] = self.grid_size_var.get()
        
        if hasattr(self, 'grid_color_var'):
            self.settings["measurement"]["grid_color"] = self.grid_color_var.get()
        
        if hasattr(self, 'snap_var'):
            self.settings["measurement"]["snap_to_grid"] = self.snap_var.get()
        
        # Save settings to file
        self.save_settings()
        
        # Apply settings
        self.apply_settings()
        
        # Close the settings window
        self.settings_window.destroy()
        
        # If theme changed, offer to restart
        if theme_changed:
            self.restart_application()
        else:
            # Show confirmation
            messagebox.showinfo("Settings", "Settings saved successfully!")

    def restart_application(self):
        """Restart the application to apply theme changes"""
        # Show a message about restarting
        if messagebox.askyesno(
            "Restart Required", 
            "The theme change requires restarting the application. Restart now?"
        ):
            # Save any unsaved work if needed
            if hasattr(self.editor, 'current_image') and self.editor.current_image:
                if messagebox.askyesno("Save Work", "Do you want to save your current work before restarting?"):
                    self.editor.save_image()
            
            # Close the current application
            self.editor.root.destroy()
            
            # Restart the application (this requires the main script to be properly structured)
            import sys
            import os
            os.execl(sys.executable, sys.executable, *sys.argv)

    def show_measurement_settings(self):
        """Show measurement settings in the content frame"""
        self.set_active_category("Measurement")
        self.clear_content_frame()
        
        # Title
        title = ctk.CTkLabel(
            self.content_frame,
            text="Measurement Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(anchor="w", pady=(20, 30), padx=20)
        
        # Make sure measurement settings exist in our settings dictionary
        if "measurement" not in self.settings:
            self.settings["measurement"] = {
                "default_unit": "Pixels",
                "show_rulers": True,
                "show_grid": False,
                "grid_size": 20,
                "grid_color": "#808080",
                "snap_to_grid": False
            }
        
        # Default unit setting
        unit_frame = ctk.CTkFrame(self.content_frame)
        unit_frame.pack(fill="x", padx=20, pady=10)
        
        unit_label = ctk.CTkLabel(
            unit_frame, 
            text="Default Unit:", 
            width=150,
            anchor="w"
        )
        unit_label.pack(side="left", padx=(10, 10))
        
        # Create variable for default unit
        self.unit_var = tk.StringVar(value=self.settings["measurement"]["default_unit"])
        
        unit_options = ["Pixels", "Inches", "Centimeters", "Millimeters"]
        unit_dropdown = ctk.CTkOptionMenu(
            unit_frame,
            values=unit_options,
            variable=self.unit_var,
            width=150
        )
        unit_dropdown.pack(side="left")
        
        # Ruler settings
        ruler_frame = ctk.CTkFrame(self.content_frame)
        ruler_frame.pack(fill="x", padx=20, pady=10)
        
        ruler_label = ctk.CTkLabel(
            ruler_frame, 
            text="Show Rulers:", 
            width=150,
            anchor="w"
        )
        ruler_label.pack(side="left", padx=(10, 10))
        
        # Create variable for ruler visibility
        self.ruler_var = tk.BooleanVar(value=self.settings["measurement"]["show_rulers"])
        
        ruler_switch = ctk.CTkSwitch(
            ruler_frame,
            text="",
            variable=self.ruler_var,
            onvalue=True,
            offvalue=False
        )
        ruler_switch.pack(side="left")
        
        # Grid settings section
        grid_section = ctk.CTkFrame(self.content_frame)
        grid_section.pack(fill="x", padx=20, pady=(20, 10))
        
        grid_title = ctk.CTkLabel(
            grid_section,
            text="Grid Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        grid_title.pack(anchor="w", padx=10, pady=10)
        
        # Show grid setting
        grid_show_frame = ctk.CTkFrame(grid_section)
        grid_show_frame.pack(fill="x", padx=10, pady=5)
        
        grid_show_label = ctk.CTkLabel(
            grid_show_frame, 
            text="Show Grid:", 
            width=150,
            anchor="w"
        )
        grid_show_label.pack(side="left", padx=(10, 10))
        
        # Create variable for grid visibility
        self.grid_show_var = tk.BooleanVar(value=self.settings["measurement"]["show_grid"])
        
        grid_show_switch = ctk.CTkSwitch(
            grid_show_frame,
            text="",
            variable=self.grid_show_var,
            onvalue=True,
            offvalue=False,
            command=self.update_grid_settings_state
        )
        grid_show_switch.pack(side="left")
        
        # Grid size setting
        grid_size_frame = ctk.CTkFrame(grid_section)
        grid_size_frame.pack(fill="x", padx=10, pady=5)
        
        grid_size_label = ctk.CTkLabel(
            grid_size_frame, 
            text="Grid Size:", 
            width=150,
            anchor="w"
        )
        grid_size_label.pack(side="left", padx=(10, 10))
        
        # Create variable for grid size
        self.grid_size_var = tk.IntVar(value=self.settings["measurement"]["grid_size"])
        
        grid_size_options = [5, 10, 15, 20, 25, 50, 100]
        self.grid_size_dropdown = ctk.CTkOptionMenu(
            grid_size_frame,
            values=[str(x) for x in grid_size_options],
            variable=tk.StringVar(value=str(self.grid_size_var.get())),
            command=lambda x: self.grid_size_var.set(int(x)),
            width=150,
            state="normal" if self.grid_show_var.get() else "disabled"
        )
        self.grid_size_dropdown.pack(side="left")
        
        # Grid color setting
        grid_color_frame = ctk.CTkFrame(grid_section)
        grid_color_frame.pack(fill="x", padx=10, pady=5)
        
        grid_color_label = ctk.CTkLabel(
            grid_color_frame, 
            text="Grid Color:", 
            width=150,
            anchor="w"
        )
        grid_color_label.pack(side="left", padx=(10, 10))
        
        # Create variable for grid color
        self.grid_color_var = tk.StringVar(value=self.settings["measurement"]["grid_color"])
        
        # Color options
        color_options = [
            ("#808080", "Gray"), 
            ("#000000", "Black"), 
            ("#FF0000", "Red"), 
            ("#0000FF", "Blue"),
            ("#00FF00", "Green")
        ]
        
        # Create a frame for color options
        color_options_frame = ctk.CTkFrame(grid_color_frame)
        color_options_frame.pack(side="left")
        
        # Create color radio buttons
        self.color_buttons = []
        for color_code, color_name in color_options:
            color_button = ctk.CTkRadioButton(
                color_options_frame,
                text=color_name,
                variable=self.grid_color_var,
                value=color_code,
                state="normal" if self.grid_show_var.get() else "disabled"
            )
            color_button.pack(side="left", padx=5)
            self.color_buttons.append(color_button)
        
        # Snap to grid setting
        snap_frame = ctk.CTkFrame(grid_section)
        snap_frame.pack(fill="x", padx=10, pady=5)
        
        snap_label = ctk.CTkLabel(
            snap_frame, 
            text="Snap to Grid:", 
            width=150,
            anchor="w"
        )
        snap_label.pack(side="left", padx=(10, 10))
        
        # Create variable for snap to grid
        self.snap_var = tk.BooleanVar(value=self.settings["measurement"]["snap_to_grid"])
        
        self.snap_switch = ctk.CTkSwitch(
            snap_frame,
            text="",
            variable=self.snap_var,
            onvalue=True,
            offvalue=False,
            state="normal" if self.grid_show_var.get() else "disabled"
        )
        self.snap_switch.pack(side="left")
        
        # Grid preview section
        preview_frame = ctk.CTkFrame(self.content_frame)
        preview_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        preview_label = ctk.CTkLabel(
            preview_frame, 
            text="Grid Preview", 
            font=ctk.CTkFont(weight="bold")
        )
        preview_label.pack(anchor="w", pady=(10, 10), padx=10)
        
        # Create a canvas for grid preview
        self.preview_canvas = tk.Canvas(
            preview_frame,
            width=300,
            height=150,
            bg="#ffffff",
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        self.preview_canvas.pack(pady=(0, 10), padx=10)
        
        # Draw initial grid preview
        self.update_grid_preview()
        
        # Add a button to update the preview
        update_preview_btn = ctk.CTkButton(
            preview_frame,
            text="Update Preview",
            command=self.update_grid_preview,
            width=150
        )
        update_preview_btn.pack(pady=10)

    def update_grid_settings_state(self):
        """Update the state of grid-related settings based on grid visibility"""
        state = "normal" if self.grid_show_var.get() else "disabled"
        
        # Update dropdown state
        self.grid_size_dropdown.configure(state=state)
        
        # Update color buttons state
        for button in self.color_buttons:
            button.configure(state=state)
        
        # Update snap switch state
        self.snap_switch.configure(state=state)
        
        # Update the preview
        self.update_grid_preview()

    def update_grid_preview(self):
        """Update the grid preview canvas"""
        # Clear the canvas
        self.preview_canvas.delete("all")
        
        # If grid is not shown, just return
        if not self.grid_show_var.get():
            return
        
        # Get current settings
        grid_size = self.grid_size_var.get()
        grid_color = self.grid_color_var.get()
        
        # Get canvas dimensions
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()
        
        # Draw vertical grid lines
        for x in range(0, canvas_width, grid_size):
            self.preview_canvas.create_line(x, 0, x, canvas_height, fill=grid_color, width=1)
        
        # Draw horizontal grid lines
        for y in range(0, canvas_height, grid_size):
            self.preview_canvas.create_line(0, y, canvas_width, y, fill=grid_color, width=1)
