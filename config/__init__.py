"""Configuration module for CHRONOS-MULTILOGIN"""

from .settings import Config

# Export both Config class and CONFIG instance for backward compatibility
CONFIG = Config

__all__ = ['Config', 'CONFIG']