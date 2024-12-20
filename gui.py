import os
import platform
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import ttkbootstrap as ttk  # Modern themed Tkinter
import webbrowser
import json
import re
from typing import List, Optional, Dict, Any
import dataclasses
from src.core.steam_finder import SteamPathFinder as SteamPF
from src.ui.steam_path_ui import SteamPathUI
from src.ui.header_ui import HeaderUI
from src.ui.input_sections_ui import InputSectionsUI
from src.ui.action_buttons_ui import ActionButtonsUI
from src.core.game_utils import CK3GameUtils
from src.core.mod_creator import ModCreator
from debug.debug_config import setup_logging, is_debug_mode

@dataclasses.dataclass
class ModCreationParams:
    """
    Dataclass to validate and store mod creation parameters.
    """
    mod_name: str
    short_mod_name: str
    tags: List[str]
    supported_version: Optional[str] = None

    def __post_init__(self):
        """
        Validate mod creation parameters.
        """
        # Validate mod name
        if not self.mod_name or len(self.mod_name) < 3:
            raise ValueError("Mod name must be at least 3 characters long")
        
        # Validate short mod name
        if not re.match(r'^[a-z0-9_]+$', self.short_mod_name):
            raise ValueError("Short mod name must contain only lowercase letters, numbers, and underscores")
            
class SteamModCreator:
    def __init__(self, root, debug):
        self.root = root
        self.logger = setup_logging(debug)
        self.debug = debug  # New debug flag

        # Initialize entry attributes before creating input sections
        self.mod_name_entry = None
        self.short_mod_name_entry = None
        self.supported_version_entry = None
        self.mod_tags_vars = {}

        # Log initialization
        self.logger.info(f"Initializing CK3ModCreator in {'DEBUG' if debug else 'PRODUCTION'} mode")

        self.root.title("CK3 Mod Creator")
        self.root.geometry("1000x1000")
        self.root.configure(bg='#f0f0f0')

        # Style configuration
        self.style = ttk.Style(theme='flatly')  # Modern, clean theme

        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        HeaderUI.create_header(self.main_frame)

        # Steam Path Detection
        self.steam_path = SteamPF.detect_steam_path(self.root)

        self.latest_version = CK3GameUtils.get_latest_ck3_version(self.steam_path)

        # Create Input Sections
        InputSectionsUI.create_input_sections(self.main_frame, self)

        # Create Action Buttons
        ActionButtonsUI.create_action_buttons(self.main_frame, self)

        # Steam Path Display
        SteamPathUI.create_steam_path_display(
            self.main_frame, 
            self.steam_path
        )
    
    def validate_short_mod_name(self, short_mod_name):
        # Load blocked names from JSON
        with open(os.path.join(os.path.dirname(__file__), 'src/data/blocked_short_mod_names.json'), 'r') as file:
            data = json.load(file)
            BLOCKED_SHORT_MOD_NAMES = data['BLOCKED_SHORT_MOD_NAMES']

        # Comprehensive validation checks
        if not short_mod_name:
            messagebox.showerror("Invalid Mod Name", "Short mod name cannot be empty.")
            return False

        if short_mod_name in BLOCKED_SHORT_MOD_NAMES:
            messagebox.showerror("Invalid Mod Name", 
                                f"The short mod name '{short_mod_name}' is already in use and cannot be used.")
            return False

        # Check for valid characters (lowercase, numbers, underscores)
        if not re.match(r'^[a-z0-9_]+$', short_mod_name):
            messagebox.showerror("Invalid Mod Name", 
                                "Short mod name must contain only lowercase letters, numbers, and underscores.")
            return False

        # Length constraints
        if len(short_mod_name) < 3 or len(short_mod_name) > 30:
            messagebox.showerror("Invalid Mod Name", 
                                "Short mod name must be between 3 and 30 characters long.")
            return False

        return True

    def create_mod(self):
        mod_name = self.mod_name_entry.get().strip() if self.mod_name_entry else ""
        short_mod_name = self.short_mod_name_entry.get().strip() if self.short_mod_name_entry else ""

        if not mod_name or not short_mod_name:
            messagebox.showerror("Error", "Please enter both Mod Name and Short Mod Name")
            return

        # Validation for short mod name (no spaces, lowercase)
        if ' ' in short_mod_name:
            messagebox.showerror("Error", "Short Mod Name cannot contain spaces")
            return
        if not self.validate_short_mod_name(short_mod_name):
            return

        # Collect selected tags
        selected_tags = [tag for tag, var in self.mod_tags_vars.items() if var.get()]
        # If no tags selected, use a default tag
        if not selected_tags:
            selected_tags = ["Fixes"]

        # Get the supported version from the entry
        supported_version = self.supported_version_entry.get().strip() if self.supported_version_entry else ""

        # Create mod structure
        mod_creation_result = ModCreator.create_mod_structure(
            mod_name, 
            short_mod_name, 
            selected_tags, 
            supported_version, 
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
                short_mod_name, 
                mod_name,
                status_callback=self.update_status_label
            )

            if not essentials_copy_result['success']:
                messagebox.showerror("Essentials Copy Error", essentials_copy_result['error'])
                return

        # Show success message
        messagebox.showinfo("Mod Created", f"Mod '{mod_name}' created successfully in {mod_creation_result['mod_folder_path']}")

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


def main():
    # Use ttkbootstrap for a modern look
    root = ttk.Window(themename="flatly")

     # Dynamically set debug mode
    debug_mode = is_debug_mode()
    app = SteamModCreator(root, debug=debug_mode)
    root.mainloop()

if __name__ == "__main__":
    main()