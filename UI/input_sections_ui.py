import tkinter as tk
from tkinter import ttk, messagebox

class InputSectionsUI:
    @staticmethod
    def create_input_sections(main_frame, parent_class):
        """
        Create input sections for the UI.
        
        Args:
            main_frame (tk.Frame): Parent frame to add input sections
            parent_class (SteamModCreator): Reference to the main class for callbacks
        """
        # Mod Name Section
        mod_name_frame = ttk.Frame(main_frame)
        mod_name_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(mod_name_frame, text="Mod Name:").pack(side='left')
        parent_class.mod_name_entry = ttk.Entry(mod_name_frame, width=50)
        parent_class.mod_name_entry.pack(side='left', padx=10)

        # Short Mod Name Section
        short_mod_name_frame = ttk.Frame(main_frame)
        short_mod_name_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(short_mod_name_frame, text="Short Mod Name:").pack(side='left')
        parent_class.short_mod_name_entry = ttk.Entry(short_mod_name_frame, width=50)
        parent_class.short_mod_name_entry.pack(side='left', padx=10)