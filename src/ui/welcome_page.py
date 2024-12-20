import os
import tkinter as tk
from tkinter import messagebox, ttk
from src.core.steam_finder import SteamPathFinder
from src.core.config import ConfigManager

class WelcomePage:
    def __init__(self, root):
        """
        Initialize the welcome page for Steam path configuration.
        
        Args:
            root (tk.Tk): The main application root window
        """
        self.root = root
        self.welcome_dialog = None
        self.steam_path = None

    def show(self):
        """
        Show the welcome dialog for Steam path configuration.
        
        Returns:
            Optional[str]: Confirmed Steam path or None
        """
        # Only show if it's the first startup
        if not ConfigManager.is_first_startup():
            return None

        # Create a top-level dialog
        self.welcome_dialog = tk.Toplevel(self.root)
        self.welcome_dialog.title("Welcome to CK3 Mod Creator")
        self.welcome_dialog.geometry("600x400")
        self.welcome_dialog.protocol("WM_DELETE_WINDOW", self._on_close)  # Handle window close
        self.welcome_dialog.grab_set()  # Make the dialog modal

        # Create main frame
        frame = tk.Frame(self.welcome_dialog)
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Title
        tk.Label(frame, text="Welcome to CK3 Mod Creator", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))
        tk.Label(frame, text="Let's set up your Steam installation path", font=("Helvetica", 12)).pack(pady=(0, 10))

        # Attempt to detect Steam path
        detected_path = self._detect_steam_path()

        # Steam path display
        tk.Label(frame, text="Detected Steam Path:", font=("Helvetica", 12)).pack()
        path_var = tk.StringVar(value=detected_path or "No path detected")
        path_entry = tk.Entry(frame, textvariable=path_var, width=60, state='readonly')
        path_entry.pack(pady=(0, 10))

        # Path selection methods
        def use_detected_path():
            """Use the detected Steam path"""
            if detected_path:
                self.steam_path = detected_path
                ConfigManager.set_steam_path(detected_path)
                ConfigManager.mark_startup_complete()
                self.welcome_dialog.destroy()
            else:
                messagebox.showerror("Error", "No detected path available")

        def choose_custom_path():
            """Open path selection dialog"""
            custom_path = SteamPathFinder.prompt_steam_path(self.welcome_dialog)
            if custom_path:
                path_var.set(custom_path)
                self.steam_path = custom_path
                ConfigManager.set_steam_path(custom_path)
                ConfigManager.mark_startup_complete()
                self.welcome_dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Steam path is required to proceed")

        def _on_close():
            """
            Handle window close event.
            Prevents closing without selecting a path on first startup.
            """
            if ConfigManager.is_first_startup():
                messagebox.showwarning("Warning", "Steam path is required to proceed")
            else:
                self.welcome_dialog.destroy()

        # Buttons frame
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=(20, 0))

        # Use Detected Path button (only if path exists)
        if detected_path:
            tk.Button(
                button_frame, 
                text="Use Detected Path", 
                command=use_detected_path
            ).pack(side=tk.LEFT, padx=5)

        # Choose Custom Path button
        tk.Button(
            button_frame, 
            text="Choose Custom Path", 
            command=choose_custom_path
        ).pack(side=tk.LEFT, padx=5)

        # Wait for dialog to close
        self.welcome_dialog.wait_window()

        # Return the selected path
        return self.steam_path

    def _detect_steam_path(self):
        """
        Detect Steam path with error handling.
        
        Returns:
            Optional[str]: Detected Steam path or None
        """
        try:
            # Try to find Steam path
            return SteamPathFinder.find_steam_installation_path()
        except (FileNotFoundError, OSError):
            # Return None if path cannot be detected
            return None

def show_welcome_page(root):
    """
    Convenience function to show the welcome page.
    
    Args:
        root (tk.Tk): The main application root window
    
    Returns:
        Optional[str]: Confirmed Steam path or None
    """
    welcome = WelcomePage(root)
    return welcome.show()