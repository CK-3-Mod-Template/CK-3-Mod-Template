VERSION = "0.3.0"
RELEASE_STAGE = "alpha"  # Can be 'alpha', 'beta', or 'stable'

def get_version_label():
    """
    Generate a version label with color coding based on release stage.
    
    Returns:
        tuple: (version_text, color)
    """
    version_colors = {
        'alpha': 'warning',   # Yellow/Orange
        'beta': 'info',       # Blue
        'stable': 'success'   # Green
    }
    
    color = version_colors.get(RELEASE_STAGE, 'secondary')
    version_text = f"Version {VERSION} ({RELEASE_STAGE.capitalize()})"
    
    return version_text, color