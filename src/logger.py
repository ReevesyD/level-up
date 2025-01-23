import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logger(log_to_file: bool = True) -> logging.Logger:
    """
    Set up the logger with both console and file handlers.
    
    Args:
        log_to_file: Whether to also log to a file
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger('skills_gap_analyzer')
    logger.setLevel(logging.INFO)
    
    # Create formatters
    console_formatter = logging.Formatter('%(message)s')
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Create console handler with custom formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    if log_to_file:
        # Create logs directory if it doesn't exist
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Create file handler with timestamp in filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f'analysis_{timestamp}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger
