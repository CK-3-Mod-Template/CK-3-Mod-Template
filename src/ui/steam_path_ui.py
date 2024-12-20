import tkinter as tk

class SteamPathUI:
  
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