import os
import platform
import tkinter as tk
from tkinter import messagebox, filedialog
import winreg

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
            steam_path = SteamPathFinder.find_steam_installation_path()
            return steam_path
        except (FileNotFoundError, OSError) as e:
            # If automatic detection fails, prompt user
            if root:
                steam_path = SteamPathFinder.prompt_steam_path(root)
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
        Prompt user to manually select Steam installation path.
        
        Args:
            root (tk.Tk): Root window for displaying dialogs.
        
        Returns:
            str: Selected Steam path.
        
        Raises:
            SystemExit: If no path is selected.
        """
        steam_path = filedialog.askdirectory(title="Select Steam Installation Directory")
        
        if not steam_path:
            messagebox.showerror("Error", "Steam path is required to proceed.")
            root.quit()
        
        return steam_path
    
    @staticmethod
    def create_steam_path_display(main_frame, steam_path):
        """
        Create a display for the Steam installation path.
        
        Args:
            main_frame (tk.Frame): Parent frame to add the Steam path display
            steam_path (str): Path to the Steam installation
        
        Returns:
            tk.Entry: The created Steam path display widget
        """
        # Steam Path Label
        steam_path_label = tk.Label(
            main_frame, 
            text="Steam Installation Path:", 
            font=('Helvetica', 10, 'bold')
        )
        steam_path_label.pack(fill='x', padx=10, pady=(10, 0), anchor='w')

        # Steam Path Display
        steam_path_display = tk.Entry(
            main_frame, 
            width=70, 
            font=('Consolas', 10)
        )
        steam_path_display.insert(0, steam_path or "Steam path not found")
        steam_path_display.config(state=tk.DISABLED)  # Make read-only
        steam_path_display.pack(fill='x')
        
        return steam_path_display

    @staticmethod
    def update_steam_path_display(steam_path_display, new_path):
        """
        Update the Steam path display with a new path.
        
        Args:
            steam_path_display (tk.Entry): The Steam path display widget
            new_path (str): New Steam path to display
        """
        steam_path_display.config(state=tk.NORMAL)  # Enable editing
        steam_path_display.delete(0, tk.END)
        steam_path_display.insert(0, new_path or "Steam path not found")
        steam_path_display.config(state=tk.DISABLED)  # Make read-only