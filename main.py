class InvalidFilePath(Exception):
    def __init__(self,filepath):
        super().__init__(f"source.fatal :: the file you requested to execute doesn't exist the provided directory ---> {filepath}")
    
class UndefinedFileExtension(Exception):
    def __init__(self,filepath):
        super().__init__(f"source.fatal :: arc only supports '.arc' file extensions please recheck {filepath} ---> {filepath}")

from lexer.scanner import Lexer

while True:
    command = input("~$ : ")
    command = command.strip().split()
    command_name = command[1]

    match command_name:
        case "exec": #arc exec t.arc
            filepath = command[2]
            if filepath.endswith(".arc"):
                try:
                    with open(filepath,'r') as source_file:
                        source = source_file.read()
                        _lexer = Lexer(source)
                        _tokens = _lexer.tokenise()

                        for tok in _tokens:
                            print(tok)

                except FileNotFoundError:
                    raise InvalidFilePath(filepath)
            else:
                raise UndefinedFileExtension(filepath)
                    