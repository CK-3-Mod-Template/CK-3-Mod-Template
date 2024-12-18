import tkinter as tk

class SteamPathUI:
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