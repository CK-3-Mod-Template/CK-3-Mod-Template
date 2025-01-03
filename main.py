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
from src.ui.styles import configure_application_style


def main():
    # Set up global exception handling first
    setup_exception_handling()

    # Load configuration
    config = ConfigManager.load_config()
    
    # Initialize logging
    debug = is_debug_mode()
    logger = setup_logging(
        debug_mode=debug, 
        log_level=config.get('log_level', 'INFO')
    )


    # Test logging at different levels
    # logger.critical("This is a CRITICAL level log message")
    # logger.error("This is an ERROR level log message")
    # logger.warning("This is a WARNING level log message")
    # logger.info("This is an INFO level log message")
    # logger.debug("This is a DEBUG level log message")

    logger.info(f"Initializing Main Menu in {'DEBUG' if debug else 'PRODUCTION'} mode")
    
    # Create root window
    root = tk.Tk()
    root.title("CK3 Mod Creator")
    
    
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
    
    root.mainloop()

if __name__ == "__main__":
    main()