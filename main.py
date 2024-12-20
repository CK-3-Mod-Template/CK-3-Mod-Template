import sys
import os
import tkinter as tk

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.ui.main_menu import MainMenu
from debug.debug_config import setup_logging, is_debug_mode, setup_exception_handling
from src.core.config import ConfigManager
from src.ui.welcome_page import show_welcome_page


def main():
    # Set up global exception handling first
    setup_exception_handling()
    # Initialize logging
    debug = is_debug_mode()
    logger = setup_logging(debug)

    logger.info(f"Initializing Main Menu in {'DEBUG' if debug else 'PRODUCTION'} mode")
    
    # Create root window
    root = tk.Tk()
    
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
    root.mainloop()

if __name__ == "__main__":
    main()