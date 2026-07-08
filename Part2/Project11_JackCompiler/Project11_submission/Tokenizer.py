class Tokenizer:
    # token type constants
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONSTANT = "integerConstant"
    STRING_CONSTANT = "stringConstant"

    KEYWORDS = {
        'class', 'constructor', 'function', 'method', 'field', 'static', 
        'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 
        'this', 'let', 'do', 'if', 'else', 'while', 'return'
    }

    SYMBOLS = set("{}()[].,;+-*/&|<>=~")
    
    # constructor
    def __init__(self,input_file_path):
        with open(input_file_path, "r") as f: 
            self.source = f.read() # read the whole jackfile
        self.index = 0
        self.n = len(self.source)
        self.current_token = None
        self.token_type = None

    def hasMoreTokens(self):  # return boolean
        self._skip_whitespace_and_comment()
        return self.index < self.n
    
    # this function move the tokenizer to the next token and store that
    # token as the current token
    def advance(self): 
        self._skip_whitespace_and_comment()
        if self.index >= self.n:
            return

        ch = self.source[self.index]

        if ch in self.SYMBOLS: #handling symbols
            self.current_token = ch
            self.token_type = self.SYMBOL
            self.index += 1

        elif ch == '"': # handling string constants
            self.index += 1
            start = self.index 
            
            while self.index < self.n and self.source[self.index] != '"':
                self.index += 1
            self.current_token = self.source[start:self.index]
            self.token_type = self.STRING_CONSTANT
            self.index += 1 
        
        elif ch.isdigit(): #handling int constant
            start = self.index
            while self.index < self.n and self.source[self.index].isdigit():
                self.index += 1
            self.current_token = self.source[start:self.index]
            self.token_type = self.INT_CONSTANT
        
        elif ch.isalpha() or ch == "_": #handling keyword/identifier
            start = self.index

            while self.index < self.n and (self.source[self.index].isalnum() or self.source[self.index] == "_"):
                self.index += 1
            self.current_token = self.source[start:self.index]


            if self.current_token in self.KEYWORDS:  
                self.token_type = self.KEYWORD
            else:
                self.token_type = self.IDENTIFIER

### getter methods
    def tokenType(self):
        return self.token_type
    
    def keyWord(self):
        return self.current_token
    
    def symbol(self):
        return self.current_token
    
    def identifier(self):
        return self.current_token
    
    def intVal(self):
        return int(self.current_token)
    
    def stringVal(self):
        return self.current_token
    
    #skips whitespaces and comments between tokens
    def _skip_whitespace_and_comment(self):
        while self.index < self.n:

            if self.source[self.index].isspace():
                self.index += 1
            elif self.source.startswith("//",self.index):
                while self.index < self.n and self.source[self.index] != "\n":
                    self.index += 1
            elif self.source.startswith("/*", self.index):
                self.index += 2
                while self.index < self.n and not self.source.startswith("*/", self.index):
                    self.index += 1
                self.index += 2

            else:
                break

                    

