import tkinter as tk
from PIL import Image, ImageTk
import time
import sys

class SplashScreen:
    def __init__(self, duration=3):
        """
        Create a splash screen with loading animation
        
        Args:
            duration: How long to display the splash screen in seconds
        """
        self.duration = duration
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window initially
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set splash screen size
        width, height = 600, 400
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Position the window
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Set background color
        self.root.configure(bg="#1E1E1E")
        
        # Create a frame for content
        self.frame = tk.Frame(self.root, bg="#1E1E1E")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Add logo - use a text-based logo
        logo_label = tk.Label(
            self.frame, 
            text="MIE",  # Modern Image Editor initials as a text logo
            font=("Arial", 72, "bold"),
            fg="#3584e4",
            bg="#1E1E1E"
        )
        logo_label.pack(pady=(50, 20))
        
        # Add application name
        app_name = tk.Label(
            self.frame, 
            text="Modern Image Editor", 
            font=("Arial", 24, "bold"),
            fg="#FFFFFF",
            bg="#1E1E1E"
        )
        app_name.pack(pady=10)
        
        # Add version
        version_label = tk.Label(
            self.frame, 
            text="Version 1.0", 
            font=("Arial", 14),
            fg="#AAAAAA",
            bg="#1E1E1E"
        )
        version_label.pack(pady=5)
        
        # Create loading bar container
        self.progress_container = tk.Frame(self.frame, bg="#333333", height=6)
        self.progress_container.pack(fill=tk.X, padx=100, pady=30)
        
        # Create progress bar
        self.progress_bar = tk.Frame(self.progress_container, bg="#3584e4", height=6, width=0)
        self.progress_bar.place(x=0, y=0)
        
        # Loading text
        self.loading_text = tk.Label(
            self.frame, 
            text="Loading...", 
            font=("Arial", 12),
            fg="#AAAAAA",
            bg="#1E1E1E"
        )
        self.loading_text.pack(pady=5)
        
        # Copyright text
        copyright_text = tk.Label(
            self.frame, 
            text="© 2023 Modern Image Editor", 
            font=("Arial", 10),
            fg="#888888",
            bg="#1E1E1E"
        )
        copyright_text.pack(side=tk.BOTTOM, pady=10)
        
        # Show the window now that it's configured
        self.root.deiconify()
        
        # Update the UI to make sure everything is drawn
        self.root.update()
        
        # Initialize progress
        self.progress = 0
        self.container_width = self.progress_container.winfo_width()
        
        # Set up the animation
        self.start_time = time.time()
        self.loading_steps = [
            "Loading resources...", 
            "Initializing tools...", 
            "Setting up workspace...", 
            "Almost ready..."
        ]
        
        # Start the animation loop
        self.animate()
    
    def animate(self):
        """Animate the loading bar and update loading text"""
        # Calculate progress based on elapsed time
        elapsed = time.time() - self.start_time
        self.progress = min(elapsed / self.duration, 1.0)
        
        # Update progress bar width
        bar_width = int(self.container_width * self.progress)
        self.progress_bar.configure(width=bar_width)
        
        # Update loading text
        step_index = min(int(self.progress * len(self.loading_steps)), len(self.loading_steps) - 1)
        self.loading_text.configure(text=self.loading_steps[step_index])
        
        # Continue animation if not complete
        if elapsed < self.duration:
            # Schedule the next animation frame
            self.root.after(50, self.animate)
        else:
            # Animation complete, show "Ready!" and schedule closing
            self.progress_bar.configure(width=self.container_width)
            self.loading_text.configure(text="Ready!")
            self.root.after(500, self.close)
    
    def close(self):
        """Close the splash screen safely"""
        # Cancel any pending after callbacks
        for after_id in self.root.tk.call('after', 'info'):
            self.root.after_cancel(after_id)
        
        # Destroy the root window
        self.root.destroy()
    
    def show(self):
        """Show the splash screen and block until it's closed"""
        self.root.mainloop()


def start_main_app():
    """Start the main application"""
    import customtkinter as ctk
    from image_editor import ModernImageEditor
    
    root = ctk.CTk()
    app = ModernImageEditor(root)
    root.mainloop()


def show_splash_and_start_app():
    """Show splash screen and then start the main application"""
    splash = SplashScreen(duration=3)
    splash.show()
    
    # After splash screen closes, start the main app
    start_main_app()


if __name__ == "__main__":
    show_splash_and_start_app()
