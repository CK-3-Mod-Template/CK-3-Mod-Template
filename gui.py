import os
import platform
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import ttkbootstrap as ttk  # Modern themed Tkinter
import webbrowser
import json

class SteamModCreator:
    def __init__(self, root, debug):
        self.root = root
        self.debug = debug  # New debug flag
        self.root.title("CK3 Mod Creator")
        self.root.geometry("1000x1000")
        self.root.configure(bg='#f0f0f0')

        # Style configuration
        self.style = ttk.Style(theme='flatly')  # Modern, clean theme

        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        self.create_header()

        # Steam Path Detection
        self.steam_path = self.detect_steam_path()

        # Create Input Sections
        self.create_input_sections()

        # Create Action Buttons
        self.create_action_buttons()

        # Steam Path Display
        self.create_steam_path_display()

    def create_header(self):
        # Title Label
        header_label = ttk.Label(
            self.main_frame, 
            text="Crusader Kings III Mod Creator", 
            font=('Helvetica', 16, 'bold'),
            foreground='#333333'
        )
        header_label.pack(pady=(0, 20))

    def create_input_sections(self):
        # Mod Name Input
        mod_name_frame = ttk.Frame(self.main_frame)
        mod_name_frame.pack(fill='x', pady=10)

        ttk.Label(mod_name_frame, text="Mod Name:", font=('Helvetica', 10)).pack(anchor='w')
        self.mod_name_entry = ttk.Entry(mod_name_frame, width=50)
        self.mod_name_entry.pack(fill='x', expand=True)
        
        # Tooltip for Mod Name
        ttk.Label(mod_name_frame, 
                  text="Enter the full name of your mod (e.g., 'Medieval Overhaul')", 
                  font=('Helvetica', 8), 
                  foreground='gray').pack(anchor='w')

        # Short Mod Name Input
        short_mod_name_frame = ttk.Frame(self.main_frame)
        short_mod_name_frame.pack(fill='x', pady=10)

        ttk.Label(short_mod_name_frame, text="Short Mod Name:", font=('Helvetica', 10)).pack(anchor='w')
        self.short_mod_name_entry = ttk.Entry(short_mod_name_frame, width=30)
        self.short_mod_name_entry.pack(fill='x', expand=True)
        
        # Tooltip for Short Mod Name
        ttk.Label(short_mod_name_frame, 
                  text="Enter a short, unique identifier for your mod (e.g., 'medieval_overhaul')", 
                  font=('Helvetica', 8), 
                  foreground='gray').pack(anchor='w')

        # Supported Version Input
        supported_version_frame = ttk.Frame(self.main_frame)
        supported_version_frame.pack(fill='x', pady=10)

        ttk.Label(supported_version_frame, text="Supported Version:", font=('Helvetica', 10)).pack(anchor='w')
        
        # Create a frame for entry and button
        version_input_frame = ttk.Frame(supported_version_frame)
        version_input_frame.pack(fill='x', expand=True)

        self.supported_version_entry = ttk.Entry(version_input_frame, width=30)
        self.supported_version_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 10))

        # Button to open Patches wiki
        open_patches_btn = ttk.Button(
            version_input_frame, 
            text="Open Patches Wiki", 
            command=lambda: webbrowser.open("https://ck3.paradoxwikis.com/Patches"),
            style='info.TButton'  # Use an info-styled button
        )
        open_patches_btn.pack(side=tk.RIGHT)

        # Tooltip for Supported Version
        ttk.Label(supported_version_frame, 
                  text="Automatically fetched latest version from launcher", 
                  font=('Helvetica', 8), 
                  foreground='gray').pack(anchor='w')

        # Mod Tags Section
        tags_frame = ttk.LabelFrame(self.main_frame, text="Mod Tags", padding="10 10 10 10")
        tags_frame.pack(fill='x', pady=10)

        # List of mod tags
        mod_tags = [
            "Alternative History", "Balance", "Bookmarks", "Character Focuses", 
            "Character Interactions", "Culture", "Decisions", "Events", "Fixes", 
            "Gameplay", "Graphics", "Historical", "Map", "Portraits", "Religion", 
            "Schemes", "Sound", "Total Conversion", "Translation", "Utilities", "Warfare"
        ]

        # Create a dictionary to store checkbox variables
        self.mod_tags_vars = {}

        # Create checkboxes in a grid layout
        for i, tag in enumerate(mod_tags):
            var = tk.BooleanVar()
            self.mod_tags_vars[tag] = var
            cb = ttk.Checkbutton(tags_frame, text=tag, variable=var)
            
            # Calculate row and column
            row = i // 3
            col = i % 3
            
            cb.grid(row=row, column=col, sticky='w', padx=5, pady=2)

        # Add some padding at the bottom of the tags frame
        tags_frame.grid_rowconfigure(len(mod_tags) // 3 + 1, weight=1)

        # Automatically fetch the latest CK3 version
        self.latest_version = self.get_latest_ck3_version()
        
        # Pre-fill the supported version entry
        if self.latest_version:
            self.supported_version_entry.insert(0, self.latest_version)

    def get_latest_ck3_version(self):
        try:
            # Construct the path to the launcher-settings.json
            launcher_settings_path = os.path.join(
                self.steam_path, 
                'steamapps', 
                'common', 
                'Crusader Kings III', 
                'launcher', 
                'launcher-settings.json'
            )

            # Check if the file exists
            if not os.path.exists(launcher_settings_path):
                print(f"Launcher settings file not found at: {launcher_settings_path}")
                return None

            # Read the JSON file
            with open(launcher_settings_path, 'r', encoding='utf-8') as file:
                settings = json.load(file)

            # Extract the rawVersion
            version = settings.get('rawVersion')

            if version:
                print(f"Found CK3 Version: {version}")
                return version
            else:
                print("No rawVersion found in launcher-settings.json")
                return None

        except Exception as e:
            # Detailed error logging
            import traceback
            print("Full Error Traceback:")
            traceback.print_exc()
            
            # If there's any error (file reading, parsing, etc.), show a message
            messagebox.showwarning("Version Fetch Error", 
                                f"Could not fetch the game version:\n{str(e)}")
            return None

    def create_action_buttons(self):
        # Button Frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill='x', pady=20)

        # Create Mod Button
        create_button = ttk.Button(
            button_frame, 
            text="Create Mod", 
            command=self.create_mod,
            style='success.TButton'  # Green success button
        )
        create_button.pack(fill='x')

    def create_steam_path_display(self):
        # Steam Path Frame
        steam_path_frame = ttk.Frame(self.main_frame)
        steam_path_frame.pack(fill='x', pady=10)

        ttk.Label(steam_path_frame, text="Steam Installation Path:", font=('Helvetica', 10)).pack(anchor='w')
        
        # Scrollable Steam Path
        steam_path_display = tk.Text(steam_path_frame, height=3, width=50, wrap=tk.WORD)
        steam_path_display.insert(tk.END, self.steam_path)
        steam_path_display.config(state=tk.DISABLED)  # Make read-only
        steam_path_display.pack(fill='x')

    def detect_steam_path(self):
        try:
            steam_path = self.find_steam_installation_path()
            return steam_path
        except (FileNotFoundError, OSError) as e:
            # If automatic detection fails, prompt user
            steam_path = self.prompt_steam_path()
            return steam_path

    def find_steam_installation_path(self, custom_path=None):
        if platform.system() == "Windows":
            try:
                import winreg
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Valve\Steam")
                #reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\WOW6432Node\Valve\Steam")
                #steam_path, _ = winreg.QueryValueEx(reg_key, "InstallPath")
                steam_path, _ = winreg.QueryValueEx(reg_key, "SteamPath")
                winreg.CloseKey(reg_key)
                return steam_path
            except FileNotFoundError:
                raise FileNotFoundError("Steam installation not found in the registry.")
        elif platform.system() == "Linux":
            if custom_path and os.path.exists(custom_path):
                return custom_path
            common_paths = [
                os.path.expanduser("~/.steam/steam"),
                os.path.expanduser("~/.local/share/Steam"),
                os.path.expanduser("~/Steam"),
                "/usr/local/games/Steam",
                "/usr/games/Steam"
            ]
            for path in common_paths:
                if os.path.exists(path):
                    return path
            raise FileNotFoundError("Steam installation not found in the default Linux paths.")
        else:
            raise OSError("Unsupported operating system")

    def prompt_steam_path(self):
        steam_path = filedialog.askdirectory(title="Select Steam Installation Directory")
        if not steam_path:
            messagebox.showerror("Error", "Steam path is required to proceed.")
            self.root.quit()
        return steam_path

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
                        d = os.path.join(dst, item)
                        
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
    app = SteamModCreator(root, debug=False)
    root.mainloop()

if __name__ == "__main__":
    main()