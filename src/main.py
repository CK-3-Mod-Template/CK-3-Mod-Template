import os
import platform
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import ttkbootstrap as ttk
import webbrowser
import json

from src.core.steam_finder import SteamPathFinder as SteamPF
from src.ui.steam_path_ui import SteamPathUI
from src.ui.header_ui import HeaderUI
from src.ui.input_sections_ui import InputSectionsUI
from src.ui.action_buttons_ui import ActionButtonsUI
from src.core.game_utils import CK3GameUtils
from src.utils.debug_utils import is_debug_mode
from src.utils.logger import setup_logger

class SteamModCreator:
    def __init__(self, root, debug=False):
        self.root = root
        self.logger = setup_logger(debug)
        self.debug = debug

        self.logger.info(f"Initializing CK3ModCreator in {'DEBUG' if debug else 'PRODUCTION'} mode")

        self.root.title("CK3 Mod Creator")
        self.root.geometry("1000x1000")
        self.root.configure(bg='#f0f0f0')

        self.style = ttk.Style(theme='flatly')

        self.main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        HeaderUI.create_header(self.main_frame)

        self.steam_path = SteamPF.detect_steam_path(self.root)
        self.latest_version = CK3GameUtils.get_latest_ck3_version(self.steam_path)

        InputSectionsUI.create_input_sections(self.main_frame, self)
        ActionButtonsUI.create_action_buttons(self.main_frame, self)

def main():
    root = ttk.Window(themename='flatly')
    app = SteamModCreator(root, debug=is_debug_mode)
    root.mainloop()

if __name__ == "__main__":
    main()