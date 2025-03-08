import logging
import os
import traceback
import datetime
from enum import Enum, auto

class LogLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

class Logger:
    """
    Handles application-wide logging to file and console.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the logger."""
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # Configure logging
        log_file = os.path.join(logs_dir, 'error.log')
        
        # Configure the root logger
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('civ_game')
        self.logger.info("Logger initialized")
    
    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)
    
    def info(self, message):
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message, exc_info=None):
        """Log an error message, optionally including exception info."""
        if exc_info:
            self.logger.error(f"{message}\n{traceback.format_exc()}")
        else:
            self.logger.error(message)
    
    def critical(self, message, exc_info=None):
        """Log a critical error message, optionally including exception info."""
        if exc_info:
            self.logger.critical(f"{message}\n{traceback.format_exc()}")
        else:
            self.logger.critical(message)

    def log_exception(self, e, context=""):
        """Log an exception with context."""
        message = f"Exception in {context}: {str(e)}"
        self.error(message, exc_info=True)


def try_except(func):
    """
    Decorator for handling exceptions in methods.
    Logs exceptions and allows program to continue.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = Logger()
            logger.log_exception(e, func.__name__)
            return None
    return wrapper
