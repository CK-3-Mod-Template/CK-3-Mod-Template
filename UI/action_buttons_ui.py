import tkinter as tk
import ttkbootstrap as ttk
import webbrowser
import os
from tkinter import messagebox, simpledialog
from CK3_utils.game_utils import CK3GameUtils

class ActionButtonsUI:
    @staticmethod
    def show_coming_soon_dialog(feature_name):
        """
        Display a coming soon dialog for unimplemented features.
        
        Args:
            feature_name (str): Name of the feature to be displayed
        """
        dialog = tk.Toplevel()
        dialog.title("Coming Soon!")
        dialog.geometry("700x500")
        dialog.resizable(False, False)

        # Create a frame with padding
        frame = ttk.Frame(dialog, padding="20 20 20 20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Feature name label
        title_label = ttk.Label(
            frame, 
            text=f"{feature_name} Template", 
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=(0, 10))

        # Description
        desc_label = ttk.Label(
            frame, 
            text="This feature is currently under development.\n\n"
                 "We're working hard to bring you innovative modding tools!\n\n"
                 "Stay tuned for future updates.",
            wraplength=360,
            justify=tk.CENTER
        )
        desc_label.pack(pady=(0, 20))

        # Roadmap button
        roadmap_btn = ttk.Button(
            frame, 
            text="View Roadmap", 
            command=lambda: webbrowser.open("https://github.com/YourProject/roadmap"),
            style='info.TButton'
        )
        roadmap_btn.pack(pady=(0, 10))

        # Close button
        close_btn = ttk.Button(
            frame, 
            text="Close", 
            command=dialog.destroy,
            style='secondary.TButton'
        )
        close_btn.pack()

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

        # Advanced Mod Tools Button (Template)
        advanced_tools_btn = ttk.Button(
            action_buttons_frame, 
            text="Advanced Mod Tools", 
            command=lambda: ActionButtonsUI.show_coming_soon_dialog("Advanced Mod Tools"),
            style='danger.TButton'  # Use a danger-styled button to indicate advanced/experimental features
        )
        advanced_tools_btn.pack(side=tk.LEFT, padx=5, expand=True, fill='x')

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