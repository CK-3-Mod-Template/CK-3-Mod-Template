import tkinter as tk
import ttkbootstrap as ttk
import webbrowser
import os
from tkinter import messagebox
from CK3_utils.game_utils import CK3GameUtils

class ActionButtonsUI:
    @staticmethod
    def create_action_buttons(main_frame, parent_class):
        """
        Create action buttons for the mod creator UI.
        
        Args:
            main_frame (ttk.Frame): Parent frame to add action buttons
            parent_class (SteamModCreator): Reference to the main class for callbacks
        """
        # Action Buttons Frame
        action_buttons_frame = ttk.Frame(main_frame)
        action_buttons_frame.pack(fill='x', pady=20)

        # Create Mod Button
        create_mod_btn = ttk.Button(
            action_buttons_frame, 
            text="Create Mod", 
            command=parent_class.create_mod,
            style='success.TButton'  # Use a success-styled button
        )
        create_mod_btn.pack(side=tk.LEFT, padx=5, expand=True, fill='x')

        # Open Mod Folder Button
        open_mod_folder_btn = ttk.Button(
            action_buttons_frame, 
            text="Open Mod Folder", 
            command=lambda: ActionButtonsUI.open_mod_folder(parent_class),
            style='info.TButton'  # Use an info-styled button
        )
        open_mod_folder_btn.pack(side=tk.LEFT, padx=5, expand=True, fill='x')

        # List Game Files Button
        list_game_files_btn = ttk.Button(
            action_buttons_frame, 
            text="List Game Files", 
            command=lambda: CK3GameUtils.list_game_files(parent_class.steam_path),
            style='warning.TButton'  # Use a warning-styled button
        )
        list_game_files_btn.pack(side=tk.LEFT, padx=5, expand=True, fill='x')

        # Help/Documentation Button
        help_btn = ttk.Button(
            action_buttons_frame, 
            text="Help", 
            command=lambda: webbrowser.open("https://ck3.paradoxwikis.com/Modding"),
            style='secondary.TButton'  # Use a secondary-styled button
        )
        help_btn.pack(side=tk.LEFT, padx=5, expand=True, fill='x')

        # Status Label
        parent_class.status_label = ttk.Label(
            main_frame, 
            text="Ready to create mod", 
            font=('Helvetica', 10), 
            foreground='green'
        )
        parent_class.status_label.pack(pady=10)

    @staticmethod
    def open_mod_folder(self):
        """
        Open the mod folder in the default file explorer.
        """
        try:
            # Use the mod directory from the class attribute
            mod_directory = self.mod_directory if hasattr(self, 'mod_directory') else os.path.join(os.getcwd(), 'Mod')
            
            # Ensure the directory exists
            os.makedirs(mod_directory, exist_ok=True)
            
            # Open the directory in the default file explorer
            os.startfile(mod_directory)
            
            # Update status label
            self.status_label.config(text=f"Opened Mod Folder: {mod_directory}", foreground='green')
        except Exception as e:
            # Handle any errors (e.g., directory not found)
            self.status_label.config(text=f"Error opening mod folder: {str(e)}", foreground='red')