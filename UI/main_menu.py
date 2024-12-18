import os
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox, filedialog
import webbrowser
import json

class MainMenu:
    def __init__(self, root, parent_app):
        """
        Initialize the Main Menu
        
        :param root: The main tkinter root window
        :param parent_app: The parent application instance (SteamModCreator)
        """
        self.root = root
        self.parent_app = parent_app
        self.current_page = None
        
        # Styling
        self.style = ttk.Style(theme='flatly')
        
        # Track mod creation status
        self.mod_created = False
        self.current_mod_path = None

    def show_create_mod_page(self):
        """
        Navigate to the mod creation page by reinitializing the parent app's mod creation interface
        """
        # Clear current view
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Recreate the entire original mod creation UI using existing UI methods
        from UI.header_ui import HeaderUI
        from UI.input_sections_ui import InputSectionsUI
        from UI.action_buttons_ui import ActionButtonsUI
        from UI.steam_path_ui import SteamPathUI

        # Recreate main frame
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.parent_app.main_frame = main_frame

        # Back to Main Menu button
        back_btn = ttk.Button(
            main_frame, 
            text="← Back to Main Menu", 
            command=self.return_to_main_menu,
            style='secondary.TButton'
        )
        back_btn.pack(side=tk.BOTTOM, pady=10)

        # Recreate all UI components using existing methods
        HeaderUI.create_header(main_frame)
        InputSectionsUI.create_input_sections(main_frame, self.parent_app)
        ActionButtonsUI.create_action_buttons(main_frame, self.parent_app)
        SteamPathUI.create_steam_path_display(
            main_frame, 
            self.parent_app.steam_path
        )

    def return_to_main_menu(self, current_window=None):
        """
        Return to the main menu from any page
        
        :param current_window: Optional window to destroy before returning to main menu
        """
        # Destroy the current window if provided
        if current_window and isinstance(current_window, tk.Toplevel):
            current_window.destroy()
        
        # Clear current view
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Recreate main menu
        self.create_main_menu()
        
    def show_update_mod_page(self):
        """
        Page for updating an existing mod
        """
        if not self.mod_created:
            messagebox.showwarning("Update Mod", "Please create a mod first.")
            return

        update_frame = ttk.Frame(self.root)
        update_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mod update options
        ttk.Label(update_frame, text="Mod Update Options", font=("Helvetica", 14)).pack(pady=10)
        
        # List edited files
        edited_files_btn = ttk.Button(
            update_frame, 
            text="List Edited Vanilla Files", 
            command=self.list_edited_vanilla_files
        )
        edited_files_btn.pack(pady=10)

    def list_edited_vanilla_files(self):
        """
        List files that have been edited from vanilla game
        """
        if not self.mod_created:
            messagebox.showwarning("Edited Files", "No mod has been created yet.")
            return

        # TODO: Implement actual file scanning logic
        edited_files = []  # Placeholder for scanned files
        
        # Create a new window to display edited files
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edited Vanilla Files")
        edit_window.geometry("400x300")
        
        # Listbox to show edited files
        files_listbox = tk.Listbox(edit_window, width=50)
        files_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        if not edited_files:
            files_listbox.insert(tk.END, "No edited files found.")
        else:
            for file in edited_files:
                files_listbox.insert(tk.END, file)

    def show_mod_management_page(self):
        """
        Mod management interface
        """
        if not self.mod_created:
            messagebox.showwarning("Mod Management", "No mod has been created yet.")
            return

        management_frame = ttk.Frame(self.root)
        management_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(management_frame, text="Mod Management", font=("Helvetica", 14)).pack(pady=10)
        
        # Mod details display
        details_frame = ttk.Frame(management_frame)
        details_frame.pack(pady=10)
        
        details = [
            f"Mod Name: {self.parent_app.mod_name_entry.get() if hasattr(self.parent_app, 'mod_name_entry') else 'N/A'}",
            f"Short Name: {self.parent_app.short_mod_name_entry.get() if hasattr(self.parent_app, 'short_mod_name_entry') else 'N/A'}",
            f"Location: {self.current_mod_path or 'Not Set'}"
        ]
        
        for detail in details:
            ttk.Label(details_frame, text=detail).pack(anchor='w')

    def toggle_debug_mode(self, debug_state):
        """
        Toggle application debug mode
        """
        self.parent_app.debug = debug_state
        messagebox.showinfo("Debug Mode", 
                             f"Debug mode {'enabled' if debug_state else 'disabled'}. "
                             "Restart the application for changes to take effect.")

    def change_theme(self, theme_name):
        """
        Change application theme
        """
        try:
            self.style.theme_use(theme_name)
            messagebox.showinfo("Theme Changed", 
                                f"Theme changed to {theme_name}. "
                                "Restart the application for full effect.")
        except Exception as e:
            messagebox.showerror("Theme Error", f"Could not change theme: {str(e)}")

    def set_mod_created(self, mod_path):
        """
        Mark mod as created and update mod path
        
        :param mod_path: Path to the created mod
        """
        self.mod_created = True
        self.current_mod_path = mod_path
        
        # Recreate main menu to update button states
        self.create_main_menu()

    def create_base_window(self, title):
        """
        Create a base window with a back button to main menu
        
        :param title: Title of the window
        :return: Tuple of (window, main_frame)
        """
        # Create a new top-level window
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("800x600")
        window.grab_set()  # Make this window modal
        
        # Main frame for content
        main_frame = ttk.Frame(window, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Back to Main Menu button
        back_btn = ttk.Button(
            main_frame, 
            text="← Back to Main Menu", 
            command=lambda: self.return_to_main_menu(window),
            style='secondary.TButton'
        )
        back_btn.pack(side=tk.BOTTOM, pady=10)
        
        return window, main_frame

    def show_help_page(self):
        """
        Open a separate window for Help & Resources
        """
        # Create base window
        help_window, help_frame = self.create_base_window("Help & Resources")
        
        # Title
        title_label = ttk.Label(
            help_frame, 
            text="CK3 Mod Creator - Help & Resources", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Help sections
        help_sections = [
            ("Getting Started", 
             "Learn how to create and manage your CK3 mods step by step."),
            ("Modding Basics", 
             "Understand the fundamentals of Crusader Kings III modding."),
            ("Advanced Techniques", 
             "Explore advanced modding techniques and best practices.")
        ]
        
        for section_title, section_desc in help_sections:
            section_frame = ttk.Frame(help_frame)
            section_frame.pack(fill='x', pady=5)
            
            ttk.Label(section_frame, text=section_title, font=("Helvetica", 12, "bold")).pack(anchor='w')
            ttk.Label(section_frame, text=section_desc, wraplength=600).pack(anchor='w')
        
        # External Links
        links_frame = ttk.Frame(help_frame)
        links_frame.pack(pady=20)
        
        links = [
            ("Official Wiki", "https://example.com/ck3-wiki"),
            ("Modding Discord", "https://discord.gg/ck3modding"),
            ("Tutorial Videos", "https://youtube.com/ck3modding")
        ]
        
        for text, url in links:
            link_btn = ttk.Button(
                links_frame, 
                text=text, 
                command=lambda u=url: webbrowser.open(u),
                style='info.TButton'
            )
            link_btn.pack(side=tk.LEFT, padx=10)

    def show_settings_page(self):
        """
        Open a separate window for Application Settings
        """
        # Create base window
        settings_window, settings_frame = self.create_base_window("Application Settings")
        
        # Title
        title_label = ttk.Label(
            settings_frame, 
            text="CK3 Mod Creator - Settings", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Debug Mode Section
        debug_frame = ttk.Frame(settings_frame)
        debug_frame.pack(fill='x', pady=10)
        
        ttk.Label(debug_frame, text="Debug Mode", font=("Helvetica", 12, "bold")).pack(anchor='w')
        
        debug_var = tk.BooleanVar(value=self.parent_app.debug)
        debug_check = ttk.Checkbutton(
            debug_frame, 
            text="Enable Detailed Logging", 
            variable=debug_var,
            command=lambda: self.toggle_debug_mode(debug_var.get())
        )
        debug_check.pack(anchor='w')
        
        # Theme Selection Section
        theme_frame = ttk.Frame(settings_frame)
        theme_frame.pack(fill='x', pady=10)
        
        ttk.Label(theme_frame, text="Application Theme", font=("Helvetica", 12, "bold")).pack(anchor='w')
        
        themes = ['flatly', 'darkly', 'cosmo', 'journal', 'litera']
        theme_var = tk.StringVar(value=self.style.theme_use())
        theme_dropdown = ttk.Combobox(
            theme_frame, 
            textvariable=theme_var, 
            values=themes,
            state="readonly",
            width=30
        )
        theme_dropdown.pack(anchor='w', pady=5)
        theme_dropdown.bind('<<ComboboxSelected>>', 
                             lambda e: self.change_theme(theme_var.get()))
        
        # Mod Creation Preferences
        mod_pref_frame = ttk.Frame(settings_frame)
        mod_pref_frame.pack(fill='x', pady=10)
        
        ttk.Label(mod_pref_frame, text="Mod Creation Preferences", font=("Helvetica", 12, "bold")).pack(anchor='w')
        
        # Placeholder for future mod creation preferences
        ttk.Label(mod_pref_frame, text="More preferences coming soon!").pack(anchor='w')

    def show_mod_tools_page(self):
        """
        Open a separate window for Advanced Mod Tools
        """
        # Create base window
        tools_window, tools_frame = self.create_base_window("Advanced Mod Tools")
        
        # Title
        title_label = ttk.Label(
            tools_frame, 
            text="Advanced Mod Tools", 
            font=("Helvetica", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Tool Sections
        tool_sections = [
            ("List Game Files", 
             "Explore and analyze game files for modding", 
             self.list_game_files),
            ("Mod File Explorer", 
             "Browse and manage mod-related files", 
             self.open_mod_folder),
            ("File Comparison", 
             "Compare vanilla and modded files", 
             self.show_file_comparison),
            ("Mod Validation", 
             "Check mod compatibility and errors", 
             self.validate_mod)
        ]
        
        for title, description, command in tool_sections:
            tool_frame = ttk.Frame(tools_frame)
            tool_frame.pack(fill='x', pady=5)
            
            tool_btn = ttk.Button(
                tool_frame, 
                text=title, 
                command=command,
                style='primary.TButton'
            )
            tool_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            ttk.Label(tool_frame, text=description, wraplength=500).pack(side=tk.LEFT)

    def list_game_files(self):
        """
        List game files using CK3GameUtils
        """
        from CK3_utils.game_utils import CK3GameUtils
        
        # Create a new window to display game files
        files_window = tk.Toplevel(self.root)
        files_window.title("Game Files")
        files_window.geometry("800x600")
        
        # Listbox to show files
        files_listbox = tk.Listbox(files_window, width=100)
        files_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        try:
            # Get game files
            game_files = CK3GameUtils.list_game_files(self.parent_app.steam_path)
            
            if not game_files:
                files_listbox.insert(tk.END, "No game files found.")
            else:
                for file in game_files:
                    files_listbox.insert(tk.END, file)
        except Exception as e:
            files_listbox.insert(tk.END, f"Error listing game files: {str(e)}")

    def open_mod_folder(self):
        """
        Open the mod folder in the default file explorer
        """
        if not self.mod_created or not self.current_mod_path:
            messagebox.showwarning("Open Mod Folder", "No mod folder exists.")
            return
        
        try:
            os.startfile(self.current_mod_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open mod folder: {str(e)}")

    def show_file_comparison(self):
        """
        Show file comparison tool (placeholder)
        """
        messagebox.showinfo("File Comparison", 
                            "File comparison tool is coming soon!\n"
                            "This will help you compare vanilla and modded files.")

    def validate_mod(self):
        """
        Validate mod for potential issues
        """
        if not self.mod_created:
            messagebox.showwarning("Mod Validation", "Create a mod first.")
            return
        
        # Placeholder for mod validation logic
        validation_results = []
        
        # Create validation window
        val_window = tk.Toplevel(self.root)
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
        
        if not validation_results:
            results_listbox.insert(tk.END, "No issues found. Mod looks good!")
        else:
            for result in validation_results:
                results_listbox.insert(tk.END, result)

    def create_main_menu(self):
        """
        Create the main menu interface
        """
        # Clear existing content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main menu frame
        menu_frame = ttk.Frame(self.root, padding="20 20 20 20")
        menu_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(menu_frame, text="CK3 Mod Creator", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # Menu buttons with conditional states
        buttons = [
            ("Create New Mod", self.show_create_mod_page, True),
            ("Update Existing Mod", self.show_update_mod_page, self.mod_created),
            ("Advanced Mod Tools", self.show_mod_tools_page, True),
            ("Help & Resources", self.show_help_page, True),
            ("Mod Management", self.show_mod_management_page, self.mod_created),
            ("Settings", self.show_settings_page, True)
        ]

        for text, command, condition in buttons:
            btn = ttk.Button(
                menu_frame, 
                text=text, 
                command=command, 
                style='primary.TButton',
                state=tk.NORMAL if condition else tk.DISABLED
            )
            btn.pack(pady=10, fill='x')        