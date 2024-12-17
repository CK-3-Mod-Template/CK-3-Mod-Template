import os
import platform
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import ttkbootstrap as ttk  # Modern themed Tkinter
import webbrowser
import json
from steam_finder import SteamPathFinder as SteamPF
from UI.steam_path_ui import SteamPathUI
from UI.header_ui import HeaderUI
from UI.input_sections_ui import InputSectionsUI
from UI.action_buttons_ui import ActionButtonsUI
from CK3_utils.game_utils import CK3GameUtils
from debug.config import is_debug_mode
from debug.logger import setup_logger

class SteamModCreator:
    def __init__(self, root, debug):
        self.root = root
        self.logger = setup_logger(debug)
        self.debug = debug  # New debug flag
        
        # Log initialization
        self.logger.info(f"Initializing SteamModCreator in {'DEBUG' if debug else 'PRODUCTION'} mode")

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
  

    def create_mod(self):
        mod_name = self.mod_name_entry.get().strip()
        short_mod_name = self.short_mod_name_entry.get().strip()

        if not mod_name or not short_mod_name:
            messagebox.showerror("Error", "Please enter both Mod Name and Short Mod Name")
            return

        # Validation for short mod name (no spaces, lowercase)
        if ' ' in short_mod_name:
            messagebox.showerror("Error", "Short Mod Name cannot contain spaces")
            return
        # Add this at the beginning of the create_mod method
        with open(os.path.join(os.path.dirname(__file__), 'blocked_short_mod_names.json'), 'r') as file:
            data = json.load(file)
            BLOCKED_SHORT_MOD_NAMES = data['BLOCKED_SHORT_MOD_NAMES']

        # Add this validation before creating the mod
        if short_mod_name in BLOCKED_SHORT_MOD_NAMES:
            messagebox.showerror("Invalid Mod Name", 
                                f"The short mod name '{short_mod_name}' is already in use and cannot be used.")
            return

        # Collect selected tags
        selected_tags = [tag for tag, var in self.mod_tags_vars.items() if var.get()]
        # If no tags selected, use a default tag
        if not selected_tags:
            selected_tags = ["Fixes"]

        # Get the supported version from the entry
        supported_version = self.supported_version_entry.get().strip()

        try:
            # Determine mod paths based on debug flag
            if self.debug:
                # Use local debug output path
                documents_path = os.path.join(os.path.dirname(__file__), 'debug', 'output')
            else:
                # Use Paradox Interactive Documents folder
                if platform.system() == "Windows":
                    documents_path = os.path.join(os.path.expanduser('~'), 'Documents', 'Paradox Interactive', 'Crusader Kings III', 'mod')
                elif platform.system() == "Linux":
                    documents_path = os.path.join(os.path.expanduser('~'), '.local', 'share', 'Paradox Interactive', 'Crusader Kings III', 'mod')
                else:
                    raise OSError("Unsupported operating system")

            # Ensure the mod directory exists
            os.makedirs(documents_path, exist_ok=True)

            # Create mod folder
            mod_folder_path = os.path.join(documents_path, short_mod_name)
            os.makedirs(mod_folder_path, exist_ok=True)

            # Create .mod file
            mod_file_path = os.path.join(documents_path, f"{short_mod_name}.mod")
            
            # Prepare mod file content
            mod_file_content = (
                f'version="1"\n'
                f'tags={{\n'
                + ",\n".join(f'\t"{tag}"' for tag in selected_tags) + 
                "\n}\n"
                f'name="{mod_name}"\n'
                f'supported_version="{supported_version or "TODO"}"\n'
                f'path="{mod_folder_path.replace(os.sep, "/")}"\n'
            )

            # Write .mod file
            with open(mod_file_path, 'w', encoding='utf-8') as mod_file:
                mod_file.write(mod_file_content)

            # Create descriptor.mod inside the mod folder
            descriptor_file_path = os.path.join(mod_folder_path, "descriptor.mod")
            descriptor_file_content = (
                f'version="1"\n'
                f'tags={{\n'
                + ",\n".join(f'\t"{tag}"' for tag in selected_tags) + 
                "\n}\n"
                f'name="{mod_name}"\n'
                f'supported_version="{supported_version or "TODO"}"\n'
            )

            # Write descriptor.mod file
            with open(descriptor_file_path, 'w', encoding='utf-8') as descriptor_file:
                descriptor_file.write(descriptor_file_content)

            # Copy essentials folder
            essentials_source = os.path.join(os.path.dirname(__file__), 'mod', 'essentials')
            
            # Check if essentials folder exists
            if os.path.exists(essentials_source):
                # Recursive copy function with placeholder replacement
                def copy_and_replace(src, dst):
                    # Ensure destination directory exists
                    os.makedirs(dst, exist_ok=True)
                    
                    # Iterate through all items in source directory
                    for item in os.listdir(src):
                        s = os.path.join(src, item)
                        d = os.path.join(dst, item.replace('your_mod_name_here', short_mod_name))
                        
                        if os.path.isdir(s):
                            # Recursively copy subdirectories
                            copy_and_replace(s, d)
                        else:
                            # Copy and replace placeholders for files
                            with open(s, 'r', encoding='utf-8') as source_file:
                                content = source_file.read()
                            
                            # Replace placeholders
                            content = content.replace('<your_mod_name_here>', short_mod_name)
                            
                            # Write to destination
                            with open(d, 'w', encoding='utf-8') as dest_file:
                                dest_file.write(content)

                # Copy essentials to mod folder
                copy_and_replace(essentials_source, mod_folder_path)
            
            # Show success message
            messagebox.showinfo("Mod Created", 
                                f"Mod successfully created:\n\n"
                                f"Name: {mod_name}\n"
                                f"Short Name: {short_mod_name}\n"
                                f"Location: {mod_folder_path}")

        except Exception as e:
            # Handle any errors during mod creation
            messagebox.showerror("Mod Creation Error", 
                                f"Could not create mod:\n{str(e)}")
            import traceback
            traceback.print_exc()
def main():
    # Use ttkbootstrap for a modern look
    root = ttk.Window(themename="flatly")
     # Dynamically set debug mode
    debug_mode = is_debug_mode()
    app = SteamModCreator(root, debug=debug_mode)
    root.mainloop()

if __name__ == "__main__":
    main()