import os
import sys
import logging
from datetime import datetime
import traceback
import sys



def global_exception_handler(exc_type, exc_value, exc_traceback):
    """
    Global exception handler to log unhandled exceptions.
    
    Args:
        exc_type (type): Exception type
        exc_value (Exception): Exception instance
        exc_traceback (traceback): Traceback object
    """
    logger = logging.getLogger('CK3ModCreator')
    
    # Log the full traceback
    error_msg = "Uncaught exception:\n" + "".join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)
    )
    logger.critical(error_msg)
    

    # Optionally show a user-friendly error dialog
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror(
            "Unexpected Error", 
            f"An unexpected error occurred:\n{exc_value}\n\n"
            "Please check the log files for more details."
        )
    except Exception:
        # Fallback if tkinter is not available
        print(error_msg)

def setup_exception_handling():
    """
    Set up global exception handling.
    """
    sys.excepthook = global_exception_handler

def is_debug_mode():
    """
    Determine if debug mode should be enabled.
    
    Checks environment variables and a configuration file.
    Prioritizes environment variable, then config file.
    
    Returns:
        bool: True if debug mode is enabled, False otherwise
    """
    # Check environment variable first
    env_debug = os.environ.get('CK3_MOD_DEBUG', '').lower()
    if env_debug in ['1', 'true', 'yes']:
        return True
    if env_debug in ['0', 'false', 'no']:
        return False
    
    # Check for a debug configuration file
    config_path = os.path.join(os.path.dirname(__file__), 'debug.cfg')
    
    # If running from a packaged executable or installed version, always return False
    if getattr(sys, 'frozen', False) or hasattr(sys, '_MEIPASS'):
        return False
    
    try:
        with open(config_path, 'r') as f:
            debug_setting = f.read().strip().lower()
            return debug_setting in ['1', 'true', 'yes']
    except FileNotFoundError:
        # Create a default debug configuration file with strict access
        try:
            with open(config_path, 'w') as f:
                f.write('false')  # Default to false
            
            # Set restrictive permissions (Unix-like systems)
            try:
                os.chmod(config_path, 0o600)  # Read/write for owner only
            except Exception:
                pass  # Ignore permission setting errors
        except Exception:
            pass
        
        return False

def setup_logging(debug_mode=False, log_level: str = 'INFO'):
    """
    Set up a centralized logging configuration.
    
    Args:
        debug_mode (bool): Whether to enable debug-level logging
        log_level (str): Logging level from configuration
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(logs_dir, f'ck3_mod_creator_{timestamp}.log')

    # Map log level string to logging constant
    log_level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    # Determine the actual logging level
    actual_level = log_level_map.get(log_level.upper(), logging.INFO)
    
    # Override with debug mode if set
    if debug_mode:
        actual_level = logging.DEBUG

    # Configure logging
    logging.basicConfig(
        level=actual_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()  # Also log to console
        ]
    )

    logger = logging.getLogger('CK3ModCreator')
    return logger