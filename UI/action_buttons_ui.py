import tkinter as tk
import ttkbootstrap as ttk
import webbrowser
import os
from tkinter import messagebox

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
            command=lambda: ActionButtonsUI.list_game_files(parent_class),
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

    @staticmethod
    def list_game_files(self):
        """
        List game files and save them to a text file.
        """
        try:
            # Construct the path to the Crusader Kings III game directory
            game_dir = os.path.join(self.steam_path, 'steamapps', 'common', 'Crusader Kings III', 'game')
            
            # Check if the directory exists
            if not os.path.exists(game_dir):
                messagebox.showerror("Error", f"Game directory not found: {game_dir}")
                self.status_label.config(text=f"Error: Game directory not found", foreground='red')
                return

            # Create a list to store file paths
            file_list = []

            # Walk through the directory and its subdirectories
            for root, dirs, files in os.walk(game_dir):
                for file in files:
                    # Get the full path of the file
                    full_path = os.path.join(root, file)
                    # Get the relative path from the game directory
                    relative_path = os.path.relpath(full_path, game_dir)
                    file_list.append(relative_path)

            # Create a 'data' directory if it doesn't exist
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            os.makedirs(data_dir, exist_ok=True)

            # Define the output file path
            output_file = os.path.join(data_dir, 'vanilla_files.txt')

            # Write the file list to the text file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Total Files Found: {len(file_list)}\n\n")
                for file_path in sorted(file_list):
                    f.write(file_path + "\n")
            
            # Show a success message
            messagebox.showinfo("Success", f"Vanilla files list saved to:\n{output_file}")
            
            # Update status label
            self.status_label.config(text=f"Listed {len(file_list)} game files", foreground='green')

        except Exception as e:
            # Show an error message if file writing fails
            messagebox.showerror("Error", f"Failed to save file list:\n{str(e)}")
            self.status_label.config(text=f"Error listing game files: {str(e)}", foreground='red')