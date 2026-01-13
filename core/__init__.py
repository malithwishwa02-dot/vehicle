"""
PROMETHEUS-CORE: Core modules for temporal manipulation.
"""

__version__ = "2.0.0"
__author__ = "Security Research Team"

from .genesis import GenesisController
from .isolation import IsolationManager
from .profile import ProfileOrchestrator
from .forensic import ForensicAlignment
from .server_side import GAMPTriangulation
from .entropy import EntropyGenerator
from .safety import SafetyValidator
from .antidetect import AntiDetectionSuite

__all__ = [
    'GenesisController',
    'IsolationManager', 
    'ProfileOrchestrator',
    'ForensicAlignment',
    'GAMPTriangulation',
    'EntropyGenerator',
    'SafetyValidator',
    'AntiDetectionSuite'
]