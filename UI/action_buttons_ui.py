import tkinter as tk
import ttkbootstrap as ttk
import webbrowser
import os

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
            command=parent_class.open_mod_folder,
            style='info.TButton'  # Use an info-styled button
        )
        open_mod_folder_btn.pack(side=tk.LEFT, padx=5, expand=True, fill='x')

        # List Game Files Button
        list_game_files_btn = ttk.Button(
            action_buttons_frame, 
            text="List Game Files", 
            command=parent_class.list_game_files,
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

        # Additional methods to support the buttons
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

        @staticmethod
        def list_game_files(self):
            """
            List game files and display them in a new window or text area.
            """
            try:
                # Create a new top-level window for game files
                game_files_window = tk.Toplevel(self.root)
                game_files_window.title("Game Files")
                game_files_window.geometry("600x400")

                # Create a text widget to display game files
                game_files_text = tk.Text(game_files_window, wrap=tk.WORD, font=('Consolas', 10))
                game_files_text.pack(fill=tk.BOTH, expand=True)

                # Retrieve and display game files
                game_files = self.get_game_files()  # Assuming this method exists in the parent class
                
                # Insert game files into the text widget
                for file_path in game_files:
                    game_files_text.insert(tk.END, f"{file_path}\n")
                
                # Make the text widget read-only
                game_files_text.config(state=tk.DISABLED)

                # Update status label
                self.status_label.config(text=f"Listed {len(game_files)} game files", foreground='green')

            except Exception as e:
                # Handle any errors in listing game files
                self.status_label.config(text=f"Error listing game files: {str(e)}", foreground='red')

        # Bind the methods to the parent class
        parent_class.open_mod_folder = open_mod_folder.__get__(parent_class)
        parent_class.list_game_files = list_game_files.__get__(parent_class)