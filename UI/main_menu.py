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
            ("Open Mod Folder", self.open_mod_folder, self.mod_created),
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

    def show_create_mod_page(self):
        """
        Navigate to the mod creation page by reinitializing the parent app's mod creation interface
        """
        # Clear current view
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Reinitialize mod creation UI from parent app
        self.parent_app.create_input_sections()
        self.parent_app.create_action_buttons()

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

    def open_mod_folder(self):
        """
        Open the folder of the created mod
        """
        if not self.mod_created or not self.current_mod_path:
            messagebox.showwarning("Open Mod Folder", "No mod folder exists.")
            return
        
        try:
            os.startfile(self.current_mod_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open mod folder: {str(e)}")

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

    def show_help_page(self):
        """
        Help and resources page
        """
        help_frame = ttk.Frame(self.root)
        help_frame.pack(fill=tk.BOTH, expand=True)
        
        help_text = """
        CK3 Mod Creator - Help & Resources

        Quick Links:
        - Official Wiki
        - Community Discord
        - Modding Tutorials
        """
        
        help_label = ttk.Label(help_frame, text=help_text, wraplength=500)
        help_label.pack(pady=20)
        
        # Links
        links = [
            ("Open Wiki", "https://example.com/wiki"),
            ("Join Discord", "https://discord.gg/example"),
            ("Modding Tutorials", "https://example.com/tutorials")
        ]
        
        for text, url in links:
            link_btn = ttk.Button(
                help_frame, 
                text=text, 
                command=lambda u=url: webbrowser.open(u)
            )
            link_btn.pack(pady=5)

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

    def show_settings_page(self):
        """
        Application settings page
        """
        settings_frame = ttk.Frame(self.root)
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(settings_frame, text="Application Settings", font=("Helvetica", 14)).pack(pady=10)
        
        # Debug Mode Toggle
        debug_var = tk.BooleanVar(value=self.parent_app.debug)
        debug_check = ttk.Checkbutton(
            settings_frame, 
            text="Enable Debug Mode", 
            variable=debug_var,
            command=lambda: self.toggle_debug_mode(debug_var.get())
        )
        debug_check.pack(pady=10)
        
        # Theme Selection
        theme_label = ttk.Label(settings_frame, text="Select Theme:")
        theme_label.pack(pady=(10, 0))
        
        themes = ['flatly', 'darkly', 'cosmo', 'journal', 'litera']
        theme_var = tk.StringVar(value=self.style.theme_use())
        theme_dropdown = ttk.Combobox(
            settings_frame, 
            textvariable=theme_var, 
            values=themes,
            state="readonly"
        )
        theme_dropdown.pack(pady=10)
        theme_dropdown.bind('<<ComboboxSelected>>', 
                             lambda e: self.change_theme(theme_var.get()))

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