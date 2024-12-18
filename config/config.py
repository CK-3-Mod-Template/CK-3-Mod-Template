import os
import sys

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