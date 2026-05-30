import scanner, parser, interpreter
from scanner import *
from parser import *
from interpreter import *

source = """
dec x = 12
flux x = 123
"""

lexer = Lexer(source)
tokens = lexer.tokenise()
parser = Parser(tokens)
ast = parser.parse()
evaluator = Evaluator()
result = evaluator.evaluate(ast)
print(result)