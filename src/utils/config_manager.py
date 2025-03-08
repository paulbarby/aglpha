import os
import configparser
from src.utils.logger import Logger
class ConfigManager:
    """
    Handles loading and saving of game configuration settings.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the config manager."""
        self.logger = Logger()
        self.config = configparser.ConfigParser()
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.ini')
        self.load_config()
        self.logger.info("Config manager initialized")
    

    def load_config(self):
        """Load configuration from config.ini file."""
        if os.path.exists(self.config_path):
            self.config.read(self.config_path)
            self.logger.info(f"Configuration loaded from {self.config_path}")
        else:
            self.logger.warning(f"Config file not found at {self.config_path}, using defaults")
    

    def save_config(self):
        """Save current configuration to config.ini file."""
        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)
            self.logger.info(f"Configuration saved to {self.config_path}")
    
    def get_value(self, section, key, default=None):
        """Get a configuration value, returning default if not found."""
        try:
            if section in self.config and key in self.config[section]:
                # Handle different types of values
                value = self.config[section][key]
                # Try to convert to appropriate type
                if value.lower() == 'true':
                    return True
                elif value.lower() == 'false':
                    return False
                try:
                    return float(value)
                except ValueError:
                    return value
            return default
        except Exception as e:
            self.logger.error(f"Error retrieving config value {section}.{key}: {e}")
            return default
    
    def set_value(self, section, key, value):
        """Set a configuration value and save the file."""
        try:
            if section not in self.config:
                self.config[section] = {}
            
            # Convert value to string for storage
            self.config[section][key] = str(value)
            self.save_config()
            return True
        except Exception as e:
            self.logger.error(f"Error setting config value {section}.{key}: {e}")
            return False

# Create a singleton instance
config_manager = ConfigManager()
