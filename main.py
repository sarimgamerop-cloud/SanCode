import scanner, parser, interpreter
from scanner import *
from parser import *
from interpreter import *

source = """
func add(a, b) {
  stdout(a + b)
}
add(5, 3)
"""

lexer = Lexer(source)
tokens = lexer.tokenise()
parser = Parser(tokens)
ast = parser.parse()
print(f"ast: {ast}")
evaluator = Evaluator()
evaluator.evaluate(ast)
