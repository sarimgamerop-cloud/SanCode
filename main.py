import scanner,parser,ast_nodes
from scanner import *
from parser import Parser


source = """
23 + 43
"""
_lexer = Lexer(source)
_tokens = _lexer.tokenise()
_parser = Parser(_tokens)
# _parser.advance()
print(_parser.parse_expression())
