import os

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
    try:
        with open(config_path, 'r') as f:
            debug_setting = f.read().strip().lower()
            return debug_setting in ['1', 'true', 'yes']
    except FileNotFoundError:
        # Default to False if no configuration is found
        return False