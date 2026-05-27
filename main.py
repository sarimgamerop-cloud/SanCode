import scanner,parser,ast_nodes
from scanner import *
from parser import Parser



source = """
const pi =3.14
"""
_lexer = Lexer(source)
_tokens = _lexer.tokenise()
_parser = Parser(_tokens)
print(_parser.parse_statements())
