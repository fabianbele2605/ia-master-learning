"""
Tools submodule

Definiciones de herramientas disponibles para agentes
"""

from .web_search import web_search_tool
from .calculator import calculator_tool

__all__ = ["web_search_tool", "calculator_tool"]
