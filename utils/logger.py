# utils/logger.py
import logging
import colorlog

def setup_logger():
    """Configures a colorful logger for the application."""
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    ))

    logger = logging.getLogger('osint_tool')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)  # Capture everything
    return logger

# Create a global instance so other files can just 'import log'
log = setup_logger()