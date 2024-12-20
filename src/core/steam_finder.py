import os
import platform
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import winreg
from src.core.config import ConfigManager

class SteamPathFinder:
    """
    A utility class for finding Steam installation paths across different platforms.
    """

    @staticmethod
    def detect_steam_path(root=None):
        """
        Detect the Steam installation path based on the current operating system.
        
        Args:
            root (tk.Tk, optional): Root window for displaying error messages.
        
        Returns:
            str: Path to the Steam installation.
        """
        try:
            # First, check if there's a previously saved Steam path
            saved_steam_path = ConfigManager.get_steam_path()
            if saved_steam_path and os.path.exists(saved_steam_path):
                return saved_steam_path

            # If no saved path, try to detect
            steam_path = SteamPathFinder.find_steam_installation_path()
            
            # Save the detected path
            ConfigManager.set_steam_path(steam_path)
            return steam_path

        except (FileNotFoundError, OSError) as e:
            # If automatic detection fails, prompt user
            if root:
                steam_path = SteamPathFinder.prompt_steam_path(root)
                
                # Save the manually selected path
                ConfigManager.set_steam_path(steam_path)
                return steam_path
            raise

    @staticmethod
    def find_steam_installation_path(custom_path=None):
        """
        Find Steam installation path based on the operating system.
        
        Args:
            custom_path (str, optional): Custom path to check first.
        
        Returns:
            str: Path to Steam installation.
        
        Raises:
            FileNotFoundError: If Steam installation cannot be found.
            OSError: If the operating system is unsupported.
        """
        if platform.system() == "Windows":
            try:
                # Try primary registry key
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Valve\Steam")
                steam_path, _ = winreg.QueryValueEx(reg_key, "SteamPath")
                winreg.CloseKey(reg_key)
                return steam_path
            except FileNotFoundError:
                raise FileNotFoundError("Steam installation not found in the registry.")
        
        elif platform.system() == "Linux":
            # Check custom path first if provided
            if custom_path and os.path.exists(custom_path):
                return custom_path
            
            # Try common Linux Steam paths
            common_paths = [
                os.path.expanduser("~/.steam/steam"),
                os.path.expanduser("~/.local/share/Steam"),
                os.path.expanduser("~/Steam"),
                "/usr/local/games/Steam",
                "/usr/games/Steam"
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    return path
            
            raise FileNotFoundError("Steam installation not found in the default Linux paths.")
        
        else:
            raise OSError("Unsupported operating system")

    @staticmethod
    def prompt_steam_path(root):
        """
        Prompt user to select Steam installation path with an interactive dialog.
        
        Args:
            root (tk.Tk): Root window for displaying dialogs.
        
        Returns:
            str: Selected Steam path.
        
        Raises:
            SystemExit: If no path is selected.
        """
        # Create a custom dialog
        steam_path_dialog = tk.Toplevel(root)
        steam_path_dialog.title("Select Steam Installation Directory")
        steam_path_dialog.geometry("500x300")
        steam_path_dialog.grab_set()  # Make the dialog modal

        # Get Steam path history
        steam_path_history = ConfigManager.get_steam_path_history()

        # Selected path variable
        selected_path = tk.StringVar()

        # Create main frame
        frame = tk.Frame(steam_path_dialog)
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Label for instructions
        tk.Label(frame, text="Select Steam Installation Directory", font=("Helvetica", 12, "bold")).pack(pady=(0, 10))

        # Dropdown for previous paths
        tk.Label(frame, text="Previously Used Paths:").pack()
        path_dropdown = ttk.Combobox(frame, textvariable=selected_path, width=50)
        path_dropdown['values'] = steam_path_history if steam_path_history else ['No previous paths']
        path_dropdown.pack(pady=(0, 10))

        # Function to handle manual path selection
        def browse_directory():
            manual_path = filedialog.askdirectory(title="Select Steam Installation Directory")
            if manual_path:
                selected_path.set(manual_path)
                # Update dropdown values if it's a new path
                if manual_path not in path_dropdown['values']:
                    current_values = list(path_dropdown['values'])
                    current_values.insert(0, manual_path)
                    path_dropdown['values'] = current_values
                path_dropdown.set(manual_path)

        # Manual browse button
        tk.Button(frame, text="Browse", command=browse_directory).pack(pady=(0, 10))

        # Confirmation variable
        confirmed = False

        # Function to handle confirmation
        def on_confirm():
            nonlocal confirmed
            path = selected_path.get().strip()
            
            # Validate path
            if not path or path == 'No previous paths':
                messagebox.showerror("Error", "Please select a valid Steam path")
                return
            
            if not os.path.exists(path):
                messagebox.showerror("Error", f"Path does not exist: {path}")
                return
            
            confirmed = True
            steam_path_dialog.destroy()

        # Function to handle cancellation
        def on_cancel():
            nonlocal confirmed
            confirmed = False
            steam_path_dialog.destroy()

        # Confirmation buttons
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=(10, 0))
        tk.Button(button_frame, text="Confirm", command=on_confirm).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)

        # Wait for the dialog to be closed
        steam_path_dialog.wait_window()

        # Check if a path was confirmed
        if not confirmed:
            messagebox.showerror("Error", "Steam path is required to proceed.")
            root.quit()
            raise SystemExit("Steam path selection cancelled")

        # Return the selected path
        return selected_path.get()