import logging
import os
from datetime import datetime

def setup_logger(debug_mode=False):
    """
    Set up a logger with optional debug mode.
    
    Args:
        debug_mode (bool): Whether to enable debug-level logging
    
    Returns:
        logging.Logger: Configured logger
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Generate a unique log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(logs_dir, f'ck3_mod_creator_{timestamp}.log')
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if debug_mode else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also output to console
        ]
    )
    
    logger = logging.getLogger('CK3ModCreator')
    return logger