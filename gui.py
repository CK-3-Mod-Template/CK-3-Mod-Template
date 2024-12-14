import os
import platform
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import ttkbootstrap as ttk  # Modern themed Tkinter
import webbrowser
import requests
from bs4 import BeautifulSoup

class SteamModCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("CK3 Mod Creator")
        self.root.geometry("800x800")
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
                  text="Automatically fetched latest version from Patches wiki", 
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
            # Fetch the Patches wiki page
            url = "https://ck3.paradoxwikis.com/Patches"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the first version number 
            # This might need adjustment based on the exact HTML structure of the page
            version_element = soup.select_one('.wikitable tr:nth-child(2) td:first-child')
            
            if version_element:
                # Clean and return the version number
                version = version_element.get_text(strip=True)
                return version
            
            return None

        except Exception as e:
            # If there's any error (network, parsing, etc.), show a message
            messagebox.showwarning("Version Fetch Error", 
                                   f"Could not automatically fetch the latest version:\n{str(e)}")
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
                reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
                steam_path, _ = winreg.QueryValueEx(reg_key, "InstallPath")
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

        # Get the supported version from the entry
        supported_version = self.supported_version_entry.get().strip()

        # Prepare metadata output
        metadata = (
            f"name=\"{mod_name}\"\n"
            f"version=\"0.0.1\"\n"
            f"tags={{\n"
            + ",\n".join(f'\t"{tag}"' for tag in selected_tags) + 
            "\n}\n"
            f"supported_version=\"{supported_version or 'TODO'}\"\n"
            f"path=\"TODO\""
        )

        # Here you can add logic to actually create the mod
        messagebox.showinfo("Mod Creation", 
                            f"Creating mod:\n\n"
                            f"Name: {mod_name}\n"
                            f"Short Name: {short_mod_name}\n"
                            f"Steam Path: {self.steam_path}\n\n"
                            f"Selected Tags:\n{', '.join(selected_tags) if selected_tags else 'No tags selected'}\n\n"
                            f"Metadata:\n{metadata}")

def main():
    # Use ttkbootstrap for a modern look
    root = ttk.Window(themename="flatly")
    app = SteamModCreator(root)
    root.mainloop()

if __name__ == "__main__":
    main()