import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.ui.main_menu import MainMenu
import tkinter as tk

def main():
    # Initialize logging
    import logging
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Check for first-time setup or configuration
    from src.core.config import ConfigManager
    
    # Create root window
    root = tk.Tk()
    
    # Check if it's first startup
    if ConfigManager.is_first_startup():
        from src.ui.welcome_page import show_welcome_page
        steam_path = show_welcome_page(root)
        
        # If no path selected, exit the application
        if steam_path is None:
            root.quit()
            return
    else:
        # Not first startup, get saved Steam path
        steam_path = ConfigManager.get_steam_path()

    # Launch main menu
    app = MainMenu(root, steam_path)
    root.mainloop()

if __name__ == "__main__":
    main()