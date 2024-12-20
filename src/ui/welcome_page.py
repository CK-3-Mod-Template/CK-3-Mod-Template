import os
import tkinter as tk
from tkinter import messagebox, ttk
from src.core.steam_finder import SteamPathFinder
from src.core.config import ConfigManager
from src.core.game_utils import CK3GameUtils

class SetupWizard:
    def __init__(self, root):
        """
        Initialize the multi-step setup wizard.
        
        Args:
            root (tk.Tk): The main application root window
        """
        self.root = root
        self.setup_dialog = None
        self.current_step = 0
        self.steam_path = None
        self.game_version = None
        self.mod_directory = None
        self.steps = [
            self._steam_path_step,
            self._mod_directory_step,
            self._game_version_step
        ]

    def _on_close(self):
        """
        Handle window close event.
        Prevents closing without completing setup.
        """
        if ConfigManager.is_first_startup():
            messagebox.showwarning("Warning", "Setup must be completed to proceed")
        else:
            if self.setup_dialog:
                self.setup_dialog.destroy()

    def show(self):
        """
        Show the setup wizard.
        
        Returns:
            Optional[str]: Confirmed Steam path or None
        """
        # Only show if it's first startup
        if not ConfigManager.is_first_startup():
            return None

        # Create setup dialog
        self.setup_dialog = tk.Toplevel(self.root)
        self.setup_dialog.title("CK3 Mod Creator - Initial Setup")
        self.setup_dialog.geometry("600x400")
        self.setup_dialog.protocol("WM_DELETE_WINDOW", self._on_close)
        self.setup_dialog.grab_set()

        # Create main frame
        self.main_frame = tk.Frame(self.setup_dialog)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Navigation buttons frame
        self.nav_frame = tk.Frame(self.setup_dialog)
        self.nav_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

        # Next and Back buttons
        self.back_button = tk.Button(
            self.nav_frame, 
            text="Back", 
            command=self._previous_step, 
            state=tk.DISABLED
        )
        self.back_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(
            self.nav_frame, 
            text="Next", 
            command=self._next_step
        )
        self.next_button.pack(side=tk.RIGHT, padx=5)

        # Start first step
        self._run_current_step()

        # Wait for dialog to close
        self.setup_dialog.wait_window()

        return self.steam_path

    def _run_current_step(self):
        """
        Run the current setup step.
        """
        # Clear previous step's frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Run current step method
        self.steps[self.current_step]()

        # Update navigation button states
        self.back_button.config(
            state=tk.NORMAL if self.current_step > 0 else tk.DISABLED
        )
        self.next_button.config(
            text="Next" if self.current_step < len(self.steps) - 1 else "Finish"
        )

    def _next_step(self):
        """
        Proceed to the next setup step.
        """
        # Validate current step
        if not self._validate_current_step():
            return

        # Move to next step or finish setup
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._run_current_step()
        else:
            # Finish setup
            ConfigManager.mark_startup_complete()
            self.setup_dialog.destroy()

    def _previous_step(self):
        """
        Go back to the previous setup step.
        """
        if self.current_step > 0:
            self.current_step -= 1
            self._run_current_step()

    def _steam_path_step(self):
        """
        First step: Steam path selection.
        """
        # Title
        tk.Label(
            self.main_frame, 
            text="Steam Path Configuration", 
            font=("Helvetica", 16, "bold")
        ).pack(pady=(0, 20))

        # Attempt to detect Steam path
        detected_path = self._detect_steam_path()

        # Steam path display
        tk.Label(
            self.main_frame, 
            text="Detected Steam Path:", 
            font=("Helvetica", 12)
        ).pack()
        
        path_var = tk.StringVar(value=detected_path or "No path detected")
        path_entry = tk.Entry(
            self.main_frame, 
            textvariable=path_var, 
            width=60, 
            state='readonly'
        )
        path_entry.pack(pady=(0, 10))

        # Status label for user feedback
        status_var = tk.StringVar()
        status_label = tk.Label(
            self.main_frame, 
            textvariable=status_var, 
            font=("Helvetica", 10),
            fg="green"
        )
        status_label.pack(pady=(0, 10))

        # Path selection buttons
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=(20, 0))

        def use_detected_path():
            """Use the detected Steam path"""
            nonlocal detected_path
            if detected_path:
                self.steam_path = detected_path
                path_var.set(detected_path)
                status_var.set("✓ Detected Steam path selected")
                # Briefly highlight the entry
                path_entry.config(bg='light green')
                path_entry.after(1500, lambda: path_entry.config(bg='white'))
            else:
                status_var.set("✗ No detected path available")
                messagebox.showerror("Error", "No detected path available")

        def choose_custom_path():
            """Open path selection dialog"""
            nonlocal detected_path
            custom_path = SteamPathFinder.prompt_steam_path(self.setup_dialog)
            if custom_path:
                detected_path = custom_path
                path_var.set(custom_path)
                self.steam_path = custom_path
                status_var.set("✓ Custom Steam path selected")
                # Briefly highlight the entry
                path_entry.config(bg='light green')
                path_entry.after(1500, lambda: path_entry.config(bg='white'))
            else:
                status_var.set("✗ No path selected")

        # Use Detected Path button (only if path exists)
        if detected_path:
            tk.Button(
                button_frame, 
                text="Use Detected Path", 
                command=use_detected_path
            ).pack(side=tk.LEFT, padx=5)

        # Choose Custom Path button
        tk.Button(
            button_frame, 
            text="Choose Custom Path", 
            command=choose_custom_path
        ).pack(side=tk.LEFT, padx=5)

    def _game_version_step(self):
        """
        Second step: Verify game version.
        """
        # Title
        tk.Label(
            self.main_frame, 
            text="Game Version Verification", 
            font=("Helvetica", 16, "bold")
        ).pack(pady=(0, 20))

        # Try to find launcher settings
        try:
            game_version = CK3GameUtils.get_latest_ck3_version(self.steam_path)
            
            # Display game version
            tk.Label(
                self.main_frame, 
                text=f"Detected CK3 Version: {game_version}", 
                font=("Helvetica", 12)
            ).pack(pady=(0, 10))

            tk.Label(
                self.main_frame, 
                text="Game version successfully detected!", 
                font=("Helvetica", 10)
            ).pack()

        except Exception as e:
            # Version detection failed
            tk.Label(
                self.main_frame, 
                text="Could not detect game version", 
                font=("Helvetica", 12, "bold"),
                fg="red"
            ).pack(pady=(0, 10))

            tk.Label(
                self.main_frame, 
                text=f"Error: {str(e)}", 
                font=("Helvetica", 10)
            ).pack()

            # Option to re-select Steam path
            def retry_steam_path():
                """Go back to Steam path selection"""
                self.current_step = 0
                self._run_current_step()

            tk.Button(
                self.main_frame, 
                text="Retry Steam Path", 
                command=retry_steam_path
            ).pack(pady=(20, 0))

    def _detect_steam_path(self):
        """
        Detect Steam path with error handling.
        
        Returns:
            Optional[str]: Detected Steam path or None
        """
        try:
            # Try to find Steam path
            return SteamPathFinder.find_steam_installation_path()
        except (FileNotFoundError, OSError):
            # Return None if path cannot be detected
            return None

    def _mod_directory_step(self):
        """
        Second step: Detect and confirm CK3 mod directory.
        """
        # Title
        tk.Label(
            self.main_frame, 
            text="Mod Directory Configuration", 
            font=("Helvetica", 16, "bold")
        ).pack(pady=(0, 20))

        # Try to detect mod directory
        try:
            # Detect mod directory in Documents
            documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
            mod_dir = os.path.join(documents_path, 'Paradox Interactive', 'Crusader Kings III', 'mod')
            
            # Ensure directory exists
            os.makedirs(mod_dir, exist_ok=True)

            # Display mod directory
            tk.Label(
                self.main_frame, 
                text="Detected Mod Directory:", 
                font=("Helvetica", 12)
            ).pack()

            path_var = tk.StringVar(value=mod_dir)
            path_entry = tk.Entry(
                self.main_frame, 
                textvariable=path_var, 
                width=60, 
                state='readonly'
            )
            path_entry.pack(pady=(0, 10))

            # Status label for user feedback
            status_var = tk.StringVar()
            status_label = tk.Label(
                self.main_frame, 
                textvariable=status_var, 
                font=("Helvetica", 10),
                fg="green"
            )
            status_label.pack(pady=(0, 10))

            def use_detected_directory():
                """Use the detected mod directory"""
                self.mod_directory = mod_dir
                path_var.set(mod_dir)
                status_var.set("✓ Detected mod directory selected")
                # Briefly highlight the entry
                path_entry.config(bg='light green')
                path_entry.after(1500, lambda: path_entry.config(bg='white'))

            def choose_custom_directory():
                """Open directory selection dialog"""
                from tkinter import filedialog
                custom_dir = filedialog.askdirectory(
                    title="Select CK3 Mod Directory",
                    initialdir=documents_path
                )
                if custom_dir:
                    path_var.set(custom_dir)
                    self.mod_directory = custom_dir
                    status_var.set("✓ Custom mod directory selected")
                    # Briefly highlight the entry
                    path_entry.config(bg='light green')
                    path_entry.after(1500, lambda: path_entry.config(bg='white'))
                else:
                    status_var.set("✗ No directory selected")

            # Buttons frame
            button_frame = tk.Frame(self.main_frame)
            button_frame.pack(pady=(20, 0))

            # Use Detected Directory button
            tk.Button(
                button_frame, 
                text="Use Detected Directory", 
                command=use_detected_directory
            ).pack(side=tk.LEFT, padx=5)

            # Choose Custom Directory button
            tk.Button(
                button_frame, 
                text="Choose Custom Directory", 
                command=choose_custom_directory
            ).pack(side=tk.LEFT, padx=5)

        except Exception as e:
            # Directory detection failed
            tk.Label(
                self.main_frame, 
                text="Could not detect mod directory", 
                font=("Helvetica", 12, "bold"),
                fg="red"
            ).pack(pady=(0, 10))

            tk.Label(
                self.main_frame, 
                text=f"Error: {str(e)}", 
                font=("Helvetica", 10)
            ).pack()

    def _game_version_step(self):
        """
        Third step: Verify game version.
        """
        # Title
        tk.Label(
            self.main_frame, 
            text="Game Version Verification", 
            font=("Helvetica", 16, "bold")
        ).pack(pady=(0, 20))

        # Try to find launcher settings
        try:
            # Detect game version using Steam path
            game_version = CK3GameUtils.get_latest_ck3_version(self.steam_path)
            self.game_version = game_version
            
            # Display game version
            tk.Label(
                self.main_frame, 
                text=f"Detected CK3 Version: {game_version}", 
                font=("Helvetica", 12)
            ).pack(pady=(0, 10))

            tk.Label(
                self.main_frame, 
                text="Game version successfully detected!", 
                font=("Helvetica", 10)
            ).pack()

        except Exception as e:
            # Version detection failed
            tk.Label(
                self.main_frame, 
                text="Could not detect game version", 
                font=("Helvetica", 12, "bold"),
                fg="red"
            ).pack(pady=(0, 10))

            tk.Label(
                self.main_frame, 
                text=f"Error: {str(e)}", 
                font=("Helvetica", 10)
            ).pack()

            # Option to re-select Steam path
            def retry_steam_path():
                """Go back to Steam path selection"""
                self.current_step = 0
                self._run_current_step()

            tk.Button(
                self.main_frame, 
                text="Retry Steam Path", 
                command=retry_steam_path
            ).pack(pady=(20, 0))

    def _validate_current_step(self):
        """
        Validate the current setup step.
        
        Returns:
            bool: True if step is valid, False otherwise
        """
        if self.current_step == 0:  # Steam path step
            if not self.steam_path:
                messagebox.showwarning("Warning", "Please select a Steam path")
                return False
            ConfigManager.set_steam_path(self.steam_path)
        
        elif self.current_step == 1:  # Mod directory step
            if not self.mod_directory:
                messagebox.showwarning("Warning", "Please select a mod directory")
                return False
        
        return True

def show_welcome_page(root):
    """
    Convenience function to show the setup wizard.
    
    Args:
        root (tk.Tk): The main application root window
    
    Returns:
        Optional[str]: Confirmed Steam path or None
    """
    wizard = SetupWizard(root)
    return wizard.show()