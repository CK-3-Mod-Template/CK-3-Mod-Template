import tkinter as tk
import ttkbootstrap as ttk
import webbrowser
import os
import sys
import tkinter.messagebox as messagebox

from src.ui.settings_window import SettingsWindow
from src.core.config import ConfigManager
from src.version import get_version_label

class MainMenu:
    def __init__(self, root, debug=False, steam_path=None):
        # Use ttkbootstrap's Window instead of standard Tk
        self.root = root
        self.steam_path = steam_path
        self.debug = debug
        
        # Configure window
        self.root.title("CK3 Mod Template")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Create menu items
        self.create_menu_items()

    def create_menu_items(self):
        """Create menu items with dynamic styling"""
        # Clear any existing widgets in the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="CK3 Mod Template", 
            font=('Helvetica', 24, 'bold')
        )
        title_label.pack(pady=(0, 40))

        # Create buttons with ttkbootstrap styling
        buttons = [
            ("Create a Mod", self.open_mod_creator, 'primary'),
            ("Tools for Existing Mods", self.open_mod_tools, 'secondary'),
            ("Settings", self.open_settings, 'info'),
            ("Help with Modding", self.open_modding_help, 'success'),
            ("Quit", self.quit_application, 'danger')
        ]

        for text, command, style in buttons:
            btn = ttk.Button(
                self.main_frame, 
                text=text, 
                command=command,
                style=f'{style}.TButton',
                width=30
            )
            btn.pack(pady=10, padx=20)

        # Version label
        version_text, version_color = get_version_label()
        version_label = ttk.Label(
            self.main_frame, 
            text=version_text, 
            font=('Helvetica', 10),
            bootstyle=version_color  # Use ttkbootstrap's color styling
        )
        version_label.pack(side='bottom', pady=10)

    def open_mod_creator(self):
        """Open the mod creation window"""
        from src.ui.steam_mod_creator import SteamModCreator
        self.root.withdraw()  # Hide main menu
        mod_creator_window = ttk.Toplevel(self.root)
        app = SteamModCreator(mod_creator_window, self.debug, steam_path=self.steam_path)
        mod_creator_window.protocol("WM_DELETE_WINDOW", lambda: self.on_mod_creator_close(mod_creator_window))

    def on_mod_creator_close(self, window):
        """Handle closing of mod creator window"""
        window.destroy()
        self.root.deiconify()  # Show main menu again

    def open_mod_tools(self):
        """Open tools for existing mods"""
        messagebox.showinfo("Mod Tools", "Mod tools functionality coming soon!")

    def open_settings(self):
        """Open application settings with theme change support"""
        from main import configure_application_style
        settings_window = SettingsWindow(self.root, apply_callback=lambda theme: configure_application_style(self.root, theme))

    def open_modding_help(self):
        """Open modding help resources"""
        webbrowser.open("https://ck3.paradoxwikis.com/Modding")

    def quit_application(self):
        """Quit the application"""
        self.root.quit()