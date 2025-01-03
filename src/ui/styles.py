import tkinter as tk
import ttkbootstrap as ttk

def configure_application_style(root: tk.Tk, theme: str = 'flatly') -> None:
    """
    Configure the application's global style and theme.
    
    Args:
        root (tk.Tk): The main application window
        theme (str, optional): The theme to apply. Defaults to 'flatly'.
    """
    # [Existing implementation from main.py]
    if theme == 'dark':
        # Dark theme configuration
        bg_color = '#2c2c2c'
        fg_color = '#ffffff'
        
        # Configure root window
        root.configure(bg=bg_color)
        
        # Configure global styles for ttkbootstrap
        style = ttk.Style()
        style.theme_use('darkly')  # Use a dark theme from ttkbootstrap
    else:
        # Light theme configuration (default)
        bg_color = '#f0f0f0'  # Light gray background
        fg_color = '#000000'
        
        # Configure root window
        root.configure(bg=bg_color)
        
        # Configure global styles for ttkbootstrap
        style = ttk.Style()
        style.theme_use('flatly')  # Use a light theme from ttkbootstrap
    
    # Set global font
    font_style = ('Segoe UI', 10)  # Modern, clean font
    root.option_add('*Font', font_style)