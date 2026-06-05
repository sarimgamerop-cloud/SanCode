import src
from src.scanner import Lexer, InvalidTokenError, UnterminatedStringLiteral, InvalidIdentifier, InvalidFloatLiteral, UnintialisedStringLiteral
from src.parser import *
from src.interpreter import Evaluator
import sys

def run_file(filename):
    if not filename.endswith('.san'):
        print("Error: File must have .san extension")
        return
    
    try:
        with open(filename, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return
    
    try:
        lexer = Lexer(source)
        print("Input source")
        tokens = lexer.tokenise()
        print("Tokenisation Finished")
        parser = Parser(tokens)
        print("Recieved tokens")
        ast = parser.parse()
        print("Finished parsing")
        evaluator = Evaluator()
        print("Recieved AST")
        evaluator.evaluate(ast)
    except (InvalidTokenError, UnterminatedStringLiteral, InvalidIdentifier, InvalidFloatLiteral, UnintialisedStringLiteral) as e:
        print(f"{e.__class__.__name__}: {e}")
    # except Exception as e:
    #     print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.san>")
        sys.exit(1)
    
    run_file(sys.argv[1])