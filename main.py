import lexer
import parsing
from lexer.tokens import *
from lexer.scanner import *
from parsing.parser import *

source = """
-8 
"""
_lexer = Lexer(source)
_tokens = _lexer.tokenise()
_parser = Parser(_tokens)
print(_parser.parse_unary())

