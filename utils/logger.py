"""
Enhanced logging utilities for CHRONOS-MULTILOGIN v2.0
Provides color-coded console output and file logging
"""

import logging
import os
from datetime import datetime
from pathlib import Path

# Try to import colorama for colored output
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False

class ChronosLogger:
    def __init__(self, log_dir=None):
        self.log_dir = Path(log_dir) if log_dir else Path(__file__).parent.parent / "logs"
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup file logging
        log_file = self.log_dir / f'chronos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        
        logging.basicConfig(
            filename=str(log_file),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Also log to console
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)
    
    def _print_colored(self, message, color, prefix):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if COLORS_AVAILABLE:
            print(f"{color}[{timestamp}] [{prefix}] {message}{Style.RESET_ALL}")
        else:
            print(f"[{timestamp}] [{prefix}] {message}")
    
    def info(self, message):
        logging.info(message)
        color = Fore.GREEN if COLORS_AVAILABLE else ""
        self._print_colored(message, color, "INFO")
    
    def warning(self, message):
        logging.warning(message)
        color = Fore.YELLOW if COLORS_AVAILABLE else ""
        self._print_colored(message, color, "WARN")
    
    def error(self, message):
        logging.error(message)
        color = Fore.RED if COLORS_AVAILABLE else ""
        self._print_colored(message, color, "ERR")
    
    def critical(self, message):
        logging.critical(message)
        color = Fore.MAGENTA if COLORS_AVAILABLE else ""
        self._print_colored(message, color, "CRIT")
    
    def success(self, message):
        logging.info(f"[SUCCESS] {message}")
        color = Fore.CYAN if COLORS_AVAILABLE else ""
        self._print_colored(message, color, "OK")

# Global logger instance
_logger_instance = None

def get_logger():
    global _logger_instance
    if _logger_instance is None:
        from config.settings import Config
        _logger_instance = ChronosLogger(Config.LOG_DIR)
    return _logger_instance

def log(message, level="INFO"):
    """Legacy function for backward compatibility"""
    logger = get_logger()
    if level == "INFO":
        logger.info(message)
    elif level == "WARNING":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message)
    elif level == "CRITICAL":
        logger.critical(message)
    elif level == "SUCCESS":
        logger.success(message)