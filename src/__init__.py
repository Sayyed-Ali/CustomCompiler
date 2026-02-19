"""Main Package Initialization"""

from .lexer import Lexer, Token
from .parser import Parser
from .semantic import SemanticAnalyzer
from .codegen import CodeGenerator

__version__ = "1.0.0"
__all__ = ['Lexer', 'Token', 'Parser', 'SemanticAnalyzer', 'CodeGenerator']