import os
import platform
import tkinter as tk
from tkinter import messagebox, filedialog
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
        Prompt user to manually select Steam installation path.
        
        Args:
            root (tk.Tk): Root window for displaying dialogs.
        
        Returns:
            str: Selected Steam path.
        
        Raises:
            SystemExit: If no path is selected.
        """
        # Get Steam path history for potential user guidance
        steam_path_history = ConfigManager.get_steam_path_history()
        
        steam_path = filedialog.askdirectory(
            title="Select Steam Installation Directory", 
            initialdir=steam_path_history[0] if steam_path_history else None
        )
        
        if not steam_path:
            messagebox.showerror("Error", "Steam path is required to proceed.")
            root.quit()
        
        return steam_path