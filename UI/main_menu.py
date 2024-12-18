import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox, Frame

class MainMenu:
    def __init__(self, root, parent_app):
        self.root = root
        self.parent_app = parent_app
        self.current_page = None

    def create_main_menu(self):
        # Clear existing content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main menu frame
        menu_frame = ttk.Frame(self.root, padding="20 20 20 20")
        menu_frame.pack(fill=tk.BOTH, expand=True)

        # Menu buttons
        buttons = [
            ("Create Mod", self.show_create_mod_page),
            ("Update Existing Mod", self.show_update_mod_page),
            ("Help", self.show_help_page),
            ("Mod Management", self.show_mod_management_page),
            ("Settings", self.show_settings_page)
        ]

        for text, command in buttons:
            btn = ttk.Button(menu_frame, text=text, command=command, style='primary.TButton')
            btn.pack(pady=10, fill='x')

    def show_create_mod_page(self):
        # Reuse existing create mod functionality
        # This might involve re-initializing parts of the original SteamModCreator
        pass

    def show_update_mod_page(self):
        # New page to list and update existing mods
        update_frame = ttk.Frame(self.root)
        update_frame.pack(fill=tk.BOTH, expand=True)
        
        # List edited vanilla files
        ttk.Label(update_frame, text="Edited Vanilla Files").pack()
        # TODO: Implement logic to scan and list edited files

    def show_help_page(self):
        help_frame = ttk.Frame(self.root)
        help_frame.pack(fill=tk.BOTH, expand=True)
        
        help_text = """
        CK3 Mod Creator Help
        
        Quick Links:
        - Wiki: [Link to Wiki]
        - Discord: [Link to Discord]
        
        Basic Instructions:
        1. Create a new mod
        2. Customize mod details
        3. Edit files as needed
        """
        
        ttk.Label(help_frame, text=help_text, wraplength=500).pack()

    def show_mod_management_page(self):
        # Page to manage existing mods
        management_frame = ttk.Frame(self.root)
        management_frame.pack(fill=tk.BOTH, expand=True)
        
        # TODO: Implement mod listing, deletion, export functionality

    def show_settings_page(self):
        # Application settings
        settings_frame = ttk.Frame(self.root)
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add debug mode toggle, theme selection, etc.