#scanner.py
#===========================================================================================
#A lexer goes through each character and classifies each of them as their respective type of tokens
#===========================================================================================

#--------------------------------------------------------------------------------------
from tokens import *

#---Lexer Class ------------------------------------------------------------------
class Lexer:
    def __init__(self,source) -> None:
        self.source = source 
        self.line = 1
        self.pos = 0
        self.tokens = []

    def __repr__(self) -> None:
        return f"Token({Tokens.token_type}:{Tokens.token_value})"

    def current_char(self):
        """
        Returns which character the pointer is at.
        """
        if self.pos < len(self.source):
            return self.source[self.pos]
        else:
            return None

    def advance(self):
        """
        Stores & returns the current character and moves forward.
        """
        char = self.source[self.pos]
        self.pos += 1
        return char

    def peek(self):
        """
        Returns the character next to the pointer but self.pod doesn't increase.
        """
        if (self.pos + 1) < len(self.source):
            return self.source[self.pos+1]
        else:
            return None

    def add(self,token_type, line,token_value = None):
        """
        Appends the token objects into the list.
        """
        self.tokens.append(Tokens(token_type,line,token_value))

    def tokenise(self):
        """
        Main tokeniser which classifies characters as their specific category they belong too.
        """
        while self.current_char() is not None:
            char = self.current_char()

            #---Newlines---------------------
            if char == "\n":
                self.advance()
                self.line += 1

            #---Spaces----------------------
            elif char.isspace():
                self.advance()
            
            #---Equals----------------------
            elif char == '=':
                if self.peek() == '=':
                    self.add(TT_EQEQ,self.line)
                    self.advance()
                    self.advance()
                else:
                    self.add(TT_EQ,self.line)
                    self.advance()
            #---Greater--------------------
            elif char == '>':
                if self.peek() == '=':
                    self.add(TT_GTE,self.line)
                    self.advance()
                    self.advance()
                else:
                    self.add(TT_GT,self.line)
                    self.advance()
            
            #---Lesser------------------------
            elif char == '<':
                if self.peek() == '=':
                    self.add(TT_LTE,self.line)
                    self.advance()
                    self.advance()
                else:
                    self.add(TT_LT,self.line)
                    self.advance()
            
            #---Bang-------------------------
            elif char == '!':
                if self.peek() == '=':
                    self.add(TT_BANGEQ,self.line)
                    self.advance();self.advance()
                else:
                    self.add(TT_BANG,self.line)
                    self.advance()
            
            #---And--------------------------
            elif char == '&' and self.peek() == '&':
                self.add(TT_AND,self.line)
                self.advance()
                self.advance()
            
            #---Or--------------------------
            elif char == "|" and self.peek() == '|':
                self.add(TT_OR,self.line)
                self.advance()
                self.advance()
            
            #---Star-------------------------
            elif char == '*':
                if self.peek() == '*':
                    self.add(TT_STARSTAR,self.line)
                    self.advance()
                    self.advance()
                else:
                    self.add(TT_STAR,self.line)
                    self.advance()

            #---Comment---------------------
            elif char == '/':
                if self.peek() == '*':
                    self.advance()
                    self.advance()

                    while self.current_char() is not None and self.current_char() != '*' and self.peek() != '/':
                        self.advance()
                    self.advance()
                    self.advance()
                    print("Finished")

            elif char == '/':
                if self.peek() == '/':
                    self.advance()
                    while self.current_char() is not None and self.current_char() != '\n':
                        self.advance()
                    
                else:
                    self.add(TT_SLASH,self.line)
                    self.advance()

            








            else:
                raise Exception(f"Invalid token: {char}")
            
                
                    

            

        self.add(TT_EOF,self.line)            
        return self.tokens

if __name__ == "__main__":
    source = """/*
    == 
    ==
    */
    =="""
    lexer = Lexer(source)
    tokens = lexer.tokenise()
    for tok in tokens:
        print(tok)