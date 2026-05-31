import scanner, parser, interpreter
from scanner import *
from parser import *
from interpreter import *

source = """
func add(a, b) {
  return a + b
}
dec result = add(5, 3)
stdout(result)

dec x = 0
while (x < 3) {
  if (x == 1) {
    flux x = x + 1
    break
  }
  stdout(x)
  flux x = x + 1
}
"""

lexer = Lexer(source)
tokens = lexer.tokenise()
parser = Parser(tokens)
ast = parser.parse()
# print(f"ast: {ast}")
evaluator = Evaluator()
evaluator.evaluate(ast)
