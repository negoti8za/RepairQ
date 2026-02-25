"""
Logger Utility - Centralized logging for the application
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from src.config import get_app_data_dir


class AppLogger:
    """Application logger with file and console output"""
    
    _logger = None
    _log_dir = None
    
    @classmethod
    def _ensure_log_dir(cls):
        """Ensure log directory exists inside the user-writable AppData folder"""
        if cls._log_dir is None:
            log_dir = get_app_data_dir() / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            cls._log_dir = log_dir
        return cls._log_dir
    
    @classmethod
    def _setup_logger(cls):
        """Setup logger with console and file handlers"""
        if cls._logger is not None:
            return cls._logger
        
        logger = logging.getLogger("RepairQ")
        logger.setLevel(logging.DEBUG)
        
        # Ensure log directory exists
        log_dir = cls._ensure_log_dir()
        
        # File handler - all messages
        log_file = log_dir / f"repairq_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler - info and above only
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        simple_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        file_handler.setFormatter(detailed_formatter)
        console_handler.setFormatter(simple_formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        cls._logger = logger
        return logger
    
    @classmethod
    def get_logger(cls):
        """Get or create logger"""
        if cls._logger is None:
            cls._setup_logger()
        return cls._logger
    
    @classmethod
    def debug(cls, message, *args, **kwargs):
        """Log debug message"""
        cls.get_logger().debug(message, *args, **kwargs)
    
    @classmethod
    def info(cls, message, *args, **kwargs):
        """Log info message"""
        cls.get_logger().info(message, *args, **kwargs)
    
    @classmethod
    def warning(cls, message, *args, **kwargs):
        """Log warning message"""
        cls.get_logger().warning(message, *args, **kwargs)
    
    @classmethod
    def error(cls, message, *args, **kwargs):
        """Log error message"""
        cls.get_logger().error(message, *args, **kwargs)
    
    @classmethod
    def critical(cls, message, *args, **kwargs):
        """Log critical message"""
        cls.get_logger().critical(message, *args, **kwargs)
    
    @classmethod
    def exception(cls, message):
        """Log exception with traceback"""
        cls.get_logger().exception(message)
    
    @classmethod
    def get_log_directory(cls):
        """Get log directory path"""
        return cls._ensure_log_dir()
