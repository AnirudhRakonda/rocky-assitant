"""
Rocky Assistant application package.

Main entry point for the alien communication system.
"""

__version__ = "1.0.0"
__author__ = "Rocky Assistant Team"

from app.pipeline import get_assistant

__all__ = ['get_assistant']
