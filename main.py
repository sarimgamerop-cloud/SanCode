import scanner,parser,ast_nodes
from scanner import *
from parser import Parser

source = """
func add(a,b){
    if (name == "apple"){
    scan(FartHole);
    }
}
"""
# source = """
# 8/9+5*8
# 2 + 5
# """
_lexer = Lexer(source)
_tokens = _lexer.tokenise()
_parser = Parser(_tokens)
print(_parser.parse())

# for tok in _tokens: print(tok)
