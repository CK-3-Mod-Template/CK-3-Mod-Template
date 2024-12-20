import sys
import os
import tkinter as tk
import ttkbootstrap as ttk
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
    if theme == 'dark':
        # Dark theme configuration
        bg_color = '#2c2c2c'
        fg_color = '#ffffff'
        
        # Configure root window
        root.configure(bg=bg_color)
        
        # Configure global styles for ttkbootstrap
        style = ttk.Style()
        style.theme_use('darkly')  # Use a dark theme from ttkbootstrap
    else:
        # Light theme configuration (default)
        bg_color = '#f0f0f0'  # Light gray background
        fg_color = '#000000'
        
        # Configure root window
        root.configure(bg=bg_color)
        
        # Configure global styles for ttkbootstrap
        style = ttk.Style()
        style.theme_use('flatly')  # Use a light theme from ttkbootstrap
    
    # Set global font
    font_style = ('Segoe UI', 10)  # Modern, clean font
    root.option_add('*Font', font_style)

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
    # Hide the main window initially
    root.withdraw()
    
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

    # Show the main window
    root.deiconify()
    # Launch main menu
    app = MainMenu(root, debug, steam_path)
    
    # Add window resize event to save window size
    # def on_window_resize(event):
    #     ConfigManager.update_config('window_size', (event.width, event.height))
    
    #root.bind('<Configure>', on_window_resize)
    
    root.mainloop()

if __name__ == "__main__":
    main()