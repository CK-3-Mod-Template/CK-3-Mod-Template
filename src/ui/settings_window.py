import tkinter as tk
import ttkbootstrap as ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from src.core.config import ConfigManager

class SettingsWindow:
    def __init__(self, parent, apply_callback=None):
        """
        Create a settings window for application configuration
        
        Args:
            parent (tk.Tk or tk.Toplevel): Parent window
            apply_callback (callable, optional): Callback to apply settings immediately
        """
        self.parent = parent
        self.apply_callback = apply_callback
        
        # Create Toplevel window separately
        self.settings_window = ttk.Toplevel(parent)
        self.settings_window.title("Application Settings")
        self.settings_window.geometry("500x600")
        self.settings_window.resizable(False, False)
        
        # Load current configuration
        self.config = ConfigManager.load_config()
        
        # Create main settings frame
        settings_frame = ttk.Frame(self.settings_window)
        settings_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Theme Selection
        theme_label = ttk.Label(settings_frame, text="Application Theme:", font=('Helvetica', 12))
        theme_label.pack(anchor='w', pady=(0, 5))
        
        self.theme_var = tk.StringVar(value=self.config.get('theme', 'flatly'))
        theme_options = ['flatly', 'dark']
        theme_dropdown = ttk.Combobox(
            settings_frame, 
            textvariable=self.theme_var, 
            values=theme_options, 
            state='readonly',
            width=30
        )
        theme_dropdown.pack(anchor='w', pady=(0, 20))
        
        # Log Level Selection
        log_label = ttk.Label(settings_frame, text="Logging Level:", font=('Helvetica', 12))
        log_label.pack(anchor='w', pady=(0, 5))
        
        self.log_var = tk.StringVar(value=self.config.get('log_level', 'INFO'))
        log_options = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        log_dropdown = ttk.Combobox(
            settings_frame, 
            textvariable=self.log_var, 
            values=log_options, 
            state='readonly',
            width=30
        )
        log_dropdown.pack(anchor='w', pady=(0, 20))
        
        # Window Size Configuration
        size_label = ttk.Label(settings_frame, text="Default Window Size:", font=('Helvetica', 12))
        size_label.pack(anchor='w', pady=(0, 5))
        
        size_frame = ttk.Frame(settings_frame)
        size_frame.pack(anchor='w', pady=(0, 20))
        
        width_label = ttk.Label(size_frame, text="Width:")
        width_label.pack(side='left', padx=(0, 5))
        
        self.width_var = tk.IntVar(value=self.config.get('window_size', (1000, 1000))[0])
        width_entry = ttk.Entry(size_frame, textvariable=self.width_var, width=10)
        width_entry.pack(side='left', padx=(0, 10))
        
        height_label = ttk.Label(size_frame, text="Height:")
        height_label.pack(side='left', padx=(0, 5))
        
        self.height_var = tk.IntVar(value=self.config.get('window_size', (1000, 1000))[1])
        height_entry = ttk.Entry(size_frame, textvariable=self.height_var, width=10)
        height_entry.pack(side='left')
        
        # Steam Path Configuration
        steam_label = ttk.Label(settings_frame, text="Steam Path:", font=('Helvetica', 12))
        steam_label.pack(anchor='w', pady=(0, 5))
        
        steam_frame = ttk.Frame(settings_frame)
        steam_frame.pack(anchor='w', pady=(0, 20))
        
        self.steam_var = tk.StringVar(value=self.config.get('current_steam_path', ''))
        steam_entry = ttk.Entry(steam_frame, textvariable=self.steam_var, width=40)
        steam_entry.pack(side='left', padx=(0, 10))
        
        steam_browse_btn = ttk.Button(steam_frame, text="Browse", command=self.browse_steam_path)
        steam_browse_btn.pack(side='left')
        
        # Save and Cancel Buttons
        button_frame = ttk.Frame(settings_frame)
        button_frame.pack(side='bottom', fill='x', pady=(20, 0))
        
        save_btn = ttk.Button(button_frame, text="Save Settings", command=self.save_settings, style='success.TButton')
        save_btn.pack(side='right', padx=10)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.settings_window.destroy, style='danger.TButton')
        cancel_btn.pack(side='right')
    
    def browse_steam_path(self):
        """Open file dialog to browse for Steam path"""
        steam_path = filedialog.askdirectory(
            title="Select Steam Installation Directory",
            initialdir=self.steam_var.get() or ''
        )
        
        if steam_path:
            self.steam_var.set(steam_path)
    


    def save_settings(self):
        """Save the current settings to configuration"""
        try:
            # Validate window size
            try:
                width = int(self.width_var.get())
                height = int(self.height_var.get())
            except (ValueError, TypeError):
                # Fallback to default size if conversion fails
                width, height = 1000, 1000
            
            if width < 300 or height < 300:
                width, height = 1000, 1000
            
            # Safely extract theme and log level
            try:
                theme = str(self.theme_var.get())
            except Exception:
                theme = 'flatly'
            
            try:
                log_level = str(self.log_var.get())
            except Exception:
                log_level = 'INFO'
            
            # Safely extract Steam path
            try:
                steam_path = str(self.steam_var.get()).strip() or None
            except Exception:
                steam_path = None
            
            # Create a new configuration dictionary
            new_config = ConfigManager.load_config()  # Load existing config first
            
            # Update only the specific keys we want to modify
            new_config.update({
                'theme': theme,
                'log_level': log_level,
                'window_size': (width, height),
            })
            
            # Update Steam path if provided
            if steam_path:
                new_config['current_steam_path'] = steam_path
                # Update Steam path history
                steam_path_history = new_config.get('steam_path_history', [])
                if steam_path not in steam_path_history:
                    steam_path_history.insert(0, steam_path)
                    new_config['steam_path_history'] = steam_path_history[:10]
            
            # Save to config file
            ConfigManager.save_config(new_config)
            
            # Apply settings immediately if callback is provided
            if self.apply_callback:
                self.apply_callback(theme)
            
            # Show confirmation and close window
            messagebox.showinfo("Settings", "Settings saved successfully.")
            self.settings_window.destroy()
        
        except Exception as e:
            # Detailed error logging
            print(f"Error saving settings: {e}")
            import traceback
            traceback.print_exc()  # Print full stack trace
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            self.settings_window.destroy()    