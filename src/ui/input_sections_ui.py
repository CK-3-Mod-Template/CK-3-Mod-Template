import tkinter as tk
import ttkbootstrap as ttk
import webbrowser
from src.core.game_utils import CK3GameUtils

class InputSectionsUI:
    @staticmethod
    def create_input_sections(main_frame, parent_class):
        """
        Create input sections for the mod creator UI.
        
        Args:
            main_frame (ttk.Frame): Parent frame to add input sections
            parent_class (SteamModCreator): Reference to the main class for callbacks
        """
        # Mod Name Input
        mod_name_frame = ttk.Frame(main_frame)
        mod_name_frame.pack(fill='x', pady=10)

        ttk.Label(mod_name_frame, text="Mod Name:", font=('Helvetica', 10)).pack(anchor='w')
        parent_class.mod_name_entry = ttk.Entry(mod_name_frame, width=50)
        parent_class.mod_name_entry.pack(fill='x', expand=True)
        
        # Tooltip for Mod Name
        ttk.Label(mod_name_frame, 
                  text="Enter the full name of your mod (e.g., 'Medieval Overhaul')", 
                  font=('Helvetica', 8), 
                  foreground='gray').pack(anchor='w')

        # Short Mod Name Input
        short_mod_name_frame = ttk.Frame(main_frame)
        short_mod_name_frame.pack(fill='x', pady=10)

        ttk.Label(short_mod_name_frame, text="Short Mod Name:", font=('Helvetica', 10)).pack(anchor='w')
        parent_class.short_mod_name_entry = ttk.Entry(short_mod_name_frame, width=30)
        parent_class.short_mod_name_entry.pack(fill='x', expand=True)
        
        # Tooltip for Short Mod Name
        ttk.Label(short_mod_name_frame, 
                  text="Enter a short, unique identifier for your mod (e.g., 'medieval_overhaul')", 
                  font=('Helvetica', 8), 
                  foreground='gray').pack(anchor='w')

        # Supported Version Input
        supported_version_frame = ttk.Frame(main_frame)
        supported_version_frame.pack(fill='x', pady=10)

        ttk.Label(supported_version_frame, text="Supported Version:", font=('Helvetica', 10)).pack(anchor='w')
        
        # Create a frame for entry and button
        version_input_frame = ttk.Frame(supported_version_frame)
        version_input_frame.pack(fill='x', expand=True)

        parent_class.supported_version_entry = ttk.Entry(version_input_frame, width=30)
        parent_class.supported_version_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 10))

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
        tags_frame = ttk.LabelFrame(main_frame, text="Mod Tags", padding="10 10 10 10")
        tags_frame.pack(fill='x', pady=10)

        # List of mod tags
        mod_tags = [
            "Alternative History", "Balance", "Bookmarks", "Character Focuses", 
            "Character Interactions", "Culture", "Decisions", "Events", "Fixes", 
            "Gameplay", "Graphics", "Historical", "Map", "Portraits", "Religion", 
            "Schemes", "Sound", "Total Conversion", "Translation", "Utilities", "Warfare"
        ]

        # Create a dictionary to store checkbox variables
        parent_class.mod_tags_vars = {}

        # Create checkboxes in a grid layout
        for i, tag in enumerate(mod_tags):
            var = tk.BooleanVar()
            parent_class.mod_tags_vars[tag] = var
            cb = ttk.Checkbutton(tags_frame, text=tag, variable=var)
            
            # Calculate row and column
            row = i // 3
            col = i % 3
            
            cb.grid(row=row, column=col, sticky='w', padx=5, pady=2)

        # Add some padding at the bottom of the tags frame
        tags_frame.grid_rowconfigure(len(mod_tags) // 3 + 1, weight=1)

        # Automatically fetch the latest CK3 version
        latest_version = CK3GameUtils.get_latest_ck3_version(parent_class.steam_path)
        
        # Pre-fill the supported version entry
        if latest_version:
            parent_class.supported_version_entry.insert(0, latest_version)