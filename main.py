import sys
import os
import tkinter as tk
from typing import Optional, Tuple

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.ui.main_menu import MainMenu
from debug.debug_config import setup_logging, is_debug_mode, setup_exception_handling
from src.core.config import ConfigManager
from src.ui.welcome_page import show_welcome_page

def configure_application_style(root: tk.Tk, theme: str = 'flatly') -> None:
    """
    Configure the application's global style and theme.
    
    Args:
        root (tk.Tk): The main application window
        theme (str, optional): The theme to apply. Defaults to 'flatly'.
    """
    # Set global background color and font
    bg_color = '#f0f0f0'  # Light gray background
    font_style = ('Segoe UI', 10)  # Modern, clean font
    
    root.configure(bg=bg_color)
    root.option_add('*Font', font_style)
    
    # Additional theme-specific configurations can be added here
    if theme == 'dark':
        bg_color = '#2c2c2c'
        fg_color = '#ffffff'
        root.configure(bg=bg_color)
        root.option_add('*Background', bg_color)
        root.option_add('*Foreground', fg_color)

def main():
    # Set up global exception handling first
    setup_exception_handling()
    
    # Initialize logging
    debug = is_debug_mode()
    logger = setup_logging(debug)

    logger.info(f"Initializing Main Menu in {'DEBUG' if debug else 'PRODUCTION'} mode")
    
    # Create root window
    root = tk.Tk()
    root.title("CK3 Mod Creator")
    
    # Load configuration
    config = ConfigManager.load_config()
    
    # Configure application style
    configure_application_style(root, config.get('theme', 'flatly'))
    
    # Set initial window size from configuration
    window_size = config.get('window_size', (1000, 1000))
    root.geometry(f"{window_size[0]}x{window_size[1]}")
    
    # Check if it's first startup
    if ConfigManager.is_first_startup():
        steam_path = show_welcome_page(root)
        
        # If no path selected, exit the application
        if steam_path is None:
            root.quit()
            return
    else:
        # Not first startup, get saved Steam path
        steam_path = ConfigManager.get_steam_path()

    # Launch main menu
    app = MainMenu(root, debug, steam_path)
    
    # Add window resize event to save window size
    # def on_window_resize(event):
    #     ConfigManager.update_config('window_size', (event.width, event.height))
    
    #root.bind('<Configure>', on_window_resize)
    
    root.mainloop()

if __name__ == "__main__":
    main()