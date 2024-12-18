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
            command=lambda: ActionButtonsUI.list_game_files(parent_class),
            style='warning.TButton'  # Use a warning-styled button
        )
        list_game_files_btn.pack(side=tk.LEFT, padx=5, expand=True, fill='x')

        # Advanced Mod Tools Button
        advanced_tools_btn = ttk.Button(
            action_buttons_frame, 
            text="Advanced Mod Tools", 
            command=lambda: ActionButtonsUI.show_advanced_mod_tools(parent_class),
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
    def open_mod_folder(parent_class):
        """
        Open the mod folder in the default file explorer.
        
        Args:
            parent_class (SteamModCreator): Reference to the main class
        """
        try:
            # Attempt to get mod directory from main menu
            if hasattr(parent_class, 'main_menu') and parent_class.main_menu.mod_created:
                mod_directory = parent_class.main_menu.current_mod_path
            else:
                # Fallback to default mod directory
                mod_directory = os.path.join(os.path.expanduser('~'), 'Documents', 'Paradox Interactive', 'Crusader Kings III', 'mod')
            
            # Ensure the directory exists
            os.makedirs(mod_directory, exist_ok=True)
            
            # Open the directory in the default file explorer
            os.startfile(mod_directory)
            
            # Update status label if available
            if hasattr(parent_class, 'status_label'):
                parent_class.status_label.config(
                    text=f"Opened Mod Folder: {mod_directory}", 
                    foreground='green'
                )
        except Exception as e:
            # Handle any errors 
            if hasattr(parent_class, 'status_label'):
                parent_class.status_label.config(
                    text=f"Error opening mod folder: {str(e)}", 
                    foreground='red'
                )
            messagebox.showerror("Error", f"Could not open mod folder: {str(e)}")

    @staticmethod
    def list_game_files(parent_class):
        """
        List game files using CK3GameUtils
        
        Args:
            parent_class (SteamModCreator): Reference to the main class
        """
        from CK3_utils.game_utils import CK3GameUtils
        
        # Create a new window to display game files
        files_window = tk.Toplevel()
        files_window.title("Game Files")
        files_window.geometry("800x600")
        
        # Listbox to show files
        files_listbox = tk.Listbox(files_window, width=100)
        files_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        try:
            # Get game files
            game_files = CK3GameUtils.list_game_files(parent_class.steam_path)
            
            if not game_files:
                files_listbox.insert(tk.END, "No game files found.")
            else:
                for file in game_files:
                    files_listbox.insert(tk.END, file)
            
            # Update status label if available
            if hasattr(parent_class, 'status_label'):
                parent_class.status_label.config(
                    text=f"Listed {len(game_files)} game files", 
                    foreground='green'
                )
        except Exception as e:
            files_listbox.insert(tk.END, f"Error listing game files: {str(e)}")
            
            # Update status label if available
            if hasattr(parent_class, 'status_label'):
                parent_class.status_label.config(
                    text=f"Error listing game files: {str(e)}", 
                    foreground='red'
                )

    @staticmethod
    def show_advanced_mod_tools(parent_class):
        """
        Show advanced mod tools dialog
        
        Args:
            parent_class (SteamModCreator): Reference to the main class
        """
        # Create advanced tools dialog
        tools_dialog = tk.Toplevel()
        tools_dialog.title("Advanced Mod Tools")
        tools_dialog.geometry("600x400")
        
        # Tools frame
        tools_frame = ttk.Frame(tools_dialog, padding="20 20 20 20")
        tools_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tool sections
        tools = [
            ("Mod File Explorer", 
             "Browse and manage mod-related files", 
             lambda: ActionButtonsUI.open_mod_folder(parent_class)),
            ("List Game Files", 
             "Explore and analyze game files", 
             lambda: ActionButtonsUI.list_game_files(parent_class)),
            ("Mod Validation", 
             "Check mod compatibility", 
             ActionButtonsUI.validate_mod),
            ("File Comparison", 
             "Compare vanilla and modded files", 
             ActionButtonsUI.show_file_comparison)
        ]
        
        for title, description, command in tools:
            tool_frame = ttk.Frame(tools_frame)
            tool_frame.pack(fill='x', pady=5)
            
            tool_btn = ttk.Button(
                tool_frame, 
                text=title, 
                command=command,
                style='primary.TButton'
            )
            tool_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            ttk.Label(tool_frame, text=description, wraplength=400).pack(side=tk.LEFT)

    @staticmethod
    def validate_mod():
        """
        Validate mod for potential issues
        """
        # Create validation window
        val_window = tk.Toplevel()
        val_window.title("Mod Validation")
        val_window.geometry("600x400")
        
        # Results frame
        results_frame = ttk.Frame(val_window)
        results_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Results label
        results_label = ttk.Label(
            results_frame, 
            text="Mod Validation Results", 
            font=("Helvetica", 14, "bold")
        )
        results_label.pack(pady=(0, 10))
        
        # Listbox for validation results
        results_listbox = tk.Listbox(results_frame, width=70)
        results_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Placeholder validation logic
        validation_results = []
        
        if not validation_results:
            results_listbox.insert(tk.END, "No mod loaded. Create a mod first.")
        else:
            for result in validation_results:
                results_listbox.insert(tk.END, result)

    @staticmethod
    def show_file_comparison():
        """
        Show file comparison tool (placeholder)
        """
        messagebox.showinfo("File Comparison", 
                            "File comparison tool is coming soon!\n"
                            "This will help you compare vanilla and modded files.")
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