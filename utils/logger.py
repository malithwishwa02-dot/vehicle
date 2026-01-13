"""
Logging utilities for CHRONOS-MULTILOGIN
Provides centralized logging configuration
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from datetime import datetime

def setup_logger(
    name: str = "CHRONOS",
    log_dir: Optional[Path] = None,
    level: str = "INFO",
    console_output: bool = True,
    file_output: bool = True
) -> logging.Logger:
    """
    Configure and return a logger instance
    
    Args:
        name: Logger name
        log_dir: Directory for log files
        level: Logging level
        console_output: Enable console output
        file_output: Enable file output
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if file_output and log_dir:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"chronos_{timestamp}.log"
        
        file_handler = logging.handlers.RotatingFileHandler(
            filename=str(log_file),
            maxBytes=10485760,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get or create a logger with the given name"""
    return logging.getLogger(name)