import os
import platform
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import ttkbootstrap as ttk  # Modern themed Tkinter
import webbrowser
import json
import re, sys
from typing import List, Optional, Dict, Any
import dataclasses
import logging
# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
from src.core.steam_finder import SteamPathFinder as SteamPF
from src.ui.steam_path_ui import SteamPathUI
from src.ui.header_ui import HeaderUI
from src.ui.input_sections_ui import InputSectionsUI
from src.ui.action_buttons_ui import ActionButtonsUI
from src.core.game_utils import CK3GameUtils
from src.core.mod_creator import ModCreator
from debug.debug_config import setup_logging, is_debug_mode, setup_exception_handling
from src.core.config import ConfigManager
from src.core.mod_params import ModCreationParams
from src.ui.welcome_page import show_welcome_page


class SteamModCreator:
    def __init__(self, root, debug=False,steam_path=None):
        self.root = root
        self.logger = logging.getLogger('CK3ModCreator')
        self.debug = debug

        # Initialize entry attributes before creating input sections
        self.mod_name_entry = None
        self.short_mod_name_entry = None
        self.supported_version_entry = None
        self.version_info = None
        self.mod_tags_vars = {}

        # Log initialization
        self.logger.info(f"Initializing CK3ModCreator in {'DEBUG' if debug else 'PRODUCTION'} mode")

        self.root.title("CK3 Mod Creator")
        # Load window size from configuration
        window_size = ConfigManager.get_config_value('window_size', (1000, 1000))
        self.root.geometry(f"{window_size[0]}x{window_size[1]}")
        #self.root.geometry("1000x1000")
        self.root.configure(bg='#f0f0f0')

        # Style configuration
        # Use the parent's style if available, otherwise create a new style
        self.style = self.root.style if hasattr(self.root, 'style') else ttk.Style(theme='flatly')

        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        HeaderUI.create_header(self.main_frame)

        # Steam Path Detection
        self.steam_path = steam_path if steam_path else SteamPF.detect_steam_path(self.root)

        #self.latest_version = CK3GameUtils.get_latest_ck3_version(self.steam_path)
        try:
            self.version_info = CK3GameUtils.get_latest_ck3_version(self.steam_path)
            self.latest_version = CK3GameUtils.get_version_for_files(self.version_info)
            self.version_info = CK3GameUtils.get_version_info_for_ui(self.version_info)
        except Exception as e:
            self.logger.error(f"Could not detect game version: {e}")
            self.latest_version = "Unknown"

        # Create Input Sections
        InputSectionsUI.create_input_sections(self.main_frame, self)

        # Create Action Buttons
        ActionButtonsUI.create_action_buttons(self.main_frame, self)

    
    def create_mod(self):
        mod_name = self.mod_name_entry.get().strip() if self.mod_name_entry else ""
        short_mod_name = self.short_mod_name_entry.get().strip() if self.short_mod_name_entry else ""

        # Check for too short mod name
        if len(mod_name) < 3:
            messagebox.showerror("Error", "Name must be at least 3 symbols long.")
            return

        # Check for too long mod name
        if len(mod_name) > 30:
            messagebox.showwarning("Warning", "Your mod name is quite long (over 30 characters). While this won't prevent mod creation, consider using a shorter name for better compatibility.")

        if not mod_name or not short_mod_name:
            messagebox.showerror("Error", "Please enter both Mod Name and Short Mod Name")
            return

        # Collect selected tags
        selected_tags = [tag for tag, var in self.mod_tags_vars.items() if var.get()]
        # If no tags selected, use a default tag
        if not selected_tags:
            selected_tags = ["Fixes"]

        # Get the supported version from the entry
        supported_version = self.supported_version_entry.get().strip() if self.supported_version_entry else ""

        try:
            # Use ModCreationParams for validation
            mod_params = ModCreationParams(
                mod_name=mod_name,
                short_mod_name=short_mod_name,
                tags=selected_tags,
                supported_version=supported_version
            )

            # Create mod structure
            mod_creation_result = ModCreator.create_mod_structure(
                mod_params.mod_name, 
                mod_params.short_mod_name, 
                mod_params.tags, 
                mod_params.supported_version, 
                self.debug,
                status_callback=self.update_status_label
            )

            if not mod_creation_result['success']:
                messagebox.showerror("Mod Creation Error", mod_creation_result['error'])
                return

            # Copy essentials folder
            essentials_source = os.path.join(os.path.dirname(__file__), 'mod', 'essentials')
            
            # Check if essentials folder exists
            if os.path.exists(essentials_source):
                # Copy essentials to mod folder with placeholder replacement
                essentials_copy_result = ModCreator.copy_and_replace(
                    essentials_source, 
                    mod_creation_result['mod_folder_path'], 
                    mod_params.short_mod_name, 
                    mod_params.mod_name,
                    status_callback=self.update_status_label
                )

                if not essentials_copy_result['success']:
                    messagebox.showerror("Essentials Copy Error", essentials_copy_result['error'])
                    return

            # Show success message
            messagebox.showinfo("Mod Created", f"Mod '{mod_name}' created successfully in {mod_creation_result['mod_folder_path']}")
            
            # Add to recent mods
            ConfigManager.add_recent_mod(short_mod_name)

            # Optionally, show recent mods
            recent_mods = ConfigManager.get_recent_mods()
            self.logger.info(f"Recent mods: {recent_mods}")

        except ValueError as ve:
            # Catch validation errors from ModCreationParams
            messagebox.showerror("Validation Error", str(ve))
            return

    def update_status_label(self, message, is_error=False):
        """
        Update the status label with a message.
        
        Args:
            message (str): Message to display
            is_error (bool, optional): Whether the message is an error. Defaults to False.
        """
        try:
            if hasattr(self, 'status_label'):
                self.status_label.config(
                    text=message, 
                    foreground='red' if is_error else 'green'
                )
                self.logger.info(message)
            else:
                # Use debug logging if status label is not available
                if is_error:
                    self.logger.error(message)
                else:
                    self.logger.debug(message)
        except Exception as e:
            # Log any unexpected errors during status label update
            self.logger.error(f"Error updating status label: {e}")

    def on_window_resize(self, event):
        """
        Save window size when resized.
        """
        ConfigManager.update_config('window_size', (event.width, event.height))


# def main():
#     # Use ttkbootstrap for a modern look
#     root = ttk.Window(themename="flatly")
#     root.withdraw()  # Hide the main window initially

#     # Check if it's first startup
#     if ConfigManager.is_first_startup():
#         # Show only the welcome page
#         steam_path = show_welcome_page(root)
        
#         # If no path selected, exit the application
#         if steam_path is None:
#             root.quit()
#             return
#     else:
#         # Not first startup, get saved Steam path
#         steam_path = ConfigManager.get_steam_path()

#      # Dynamically set debug mode
#     debug_mode = is_debug_mode()
#     app = SteamModCreator(root, debug=debug_mode, steam_path=steam_path)
#     # Show the main window
#     root.deiconify()
#     # Bind window resize event
#     root.bind('<Configure>', app.on_window_resize)
#     root.mainloop()

# if __name__ == "__main__":
#     main()