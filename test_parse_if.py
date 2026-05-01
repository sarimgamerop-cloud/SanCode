from lexer import Lexer
from parser import Parser

# Test 1: Simple if statement
code1 = """3*59+7**4
"""
lexer1 = Lexer(code1)
tokens1 = lexer1.tokenize()
print("Test 1 - Tokens:", tokens1)

parser1 = Parser(tokens1)
ast1 = parser1.parse_expression()
print("Test 1 - AST:", ast1)


# # Test 2: if with elif
# code2 = """
# if (x > 5) {
#     out "big"
# }
# elif (x > 0) {
#     out "small"
# }
# """
# lexer2 = Lexer(code2)
# tokens2 = lexer2.tokenize()
# print("Test 2 - Tokens:", tokens2)

# parser2 = Parser(tokens2)
# ast2 = parser2.parse_statement()
# print("Test 2 - AST:", ast2)
# print()

# # Test 3: if with elif and else
# code3 = """
# if (x > 5) {
#     out "big"
# }
# elif (x > 0) {
#     out "small"
# }
# else {
#     out "negative"
# }
# """
# lexer3 = Lexer(code3)
# tokens3 = lexer3.tokenize()
# print("Test 3 - Tokens:", tokens3)

# parser3 = Parser(tokens3)
# ast3 = parser3.parse_statement()
# print("Test 3 - AST:", ast3)