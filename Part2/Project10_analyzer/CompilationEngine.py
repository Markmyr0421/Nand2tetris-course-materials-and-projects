from Tokenizer import Tokenizer

class CompilationEngine:

    #Constructor
    def __init__(self,input_file_path):
        self.tokenizer = Tokenizer(input_file_path)
        
        output_file_path = input_file_path.replace(".jack", ".xml")
        self.output = open(output_file_path,"w")

        self.indentation = 0
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

##=========================================================================

    def CompileClass(self): #'class' className '(' class VarDec* subroutineDec* ';'
        self.writeOpenTag("class")
        
        self.eat()  # class
        self.eat()  # className
        self.eat()  # {
        while self.tokenizer.current_token in {"static", "field"}:
            self.CompileClassVarDec()
        while self.tokenizer.current_token in {"constructor", "function", "method"}:
            self.CompileSubroutineDec()
        self.eat()  # }
        
        self.writeCloseTag("class")
        self.output.close()
   
   
    def CompileClassVarDec(self): #(static'|'field) type varName (,' varName)* ';'
        self.writeOpenTag("classVarDec")
        
        self.eat()  # static | field
        self.eat()  # type
        self.eat()  # varName
        while self.tokenizer.current_token == ",":
            self.eat()  # ,
            self.eat()  # varName
        self.eat()  # ;
        
        self.writeCloseTag("classVarDec")


    def CompileSubroutineDec(self): #(constructor'| 'function'| method) (void type) subroutineName
                                    #"(" parameterList ") ' subroutine Body
        self.writeOpenTag("subroutineDec")
        
        self.eat()  # constructor | function | method
        self.eat()  # void | type
        self.eat()  # subroutineName
        self.eat()  # (
        self.CompileParameterList()
        self.eat()  # )
        
        self.writeOpenTag("subroutineBody")
        
        self.eat()  # {
        while self.tokenizer.current_token == "var":
            self.CompileVarDec()
        self.CompileStatements()
        self.eat()  # }
        
        self.writeCloseTag("subroutineBody")
        
        self.writeCloseTag("subroutineDec")


    def CompileParameterList(self): #( (type varName) (,' type varName) *)?
        self.writeOpenTag("parameterList")
        if self.tokenizer.current_token != ")":
            self.eat()  
            self.eat()  

        while self.tokenizer.current_token == ",":
            self.eat()
            self.eat()  
            self.eat() 
        
        self.writeCloseTag("parameterList")



    def CompileVarDec(self): # var int x,y,z; / var boolean isClean;
        self.writeOpenTag("varDec")
        self.eat() # eat "var"
        self.eat() # eat datatype
        self.eat() # eat first var
        while self.tokenizer.current_token == ",":
            self.eat() # ","
            self.eat() # other vars
        self.eat() # ";"

        self.writeCloseTag("varDec")



##====================================================================

    def CompileStatements(self): #statement#
        self.writeOpenTag("statements")
        
        while self.tokenizer.current_token in {"let", "if", "while", "do", "return"}:
            if self.tokenizer.current_token == "let":
                self.CompileLet()
            elif self.tokenizer.current_token == "if":
                self.CompileIf()
            elif self.tokenizer.current_token == "while":
                self.CompileWhile()
            elif self.tokenizer.current_token == "do":
                self.CompileDo()
            elif self.tokenizer.current_token == "return":
               
                self.CompileReturn()
        self.writeCloseTag("statements")
    
    def CompileLet(self): # 'let' varName '=' expression ';'
        self.writeOpenTag("letStatement")
        
        self.eat()
        self.eat()

        if self.tokenizer.current_token == "[":
            self.eat()
            self.CompileExpression()
            self.eat()

        self.eat()
        self.CompileExpression()
        self.eat()

        self.writeCloseTag("letStatement")


    def CompileIf(self): #'if' ('expression) {statements} 
        self.writeOpenTag("ifStatement")
        
        self.eat()
        self.eat()
        self.CompileExpression()
        self.eat()
        self.eat()
        self.CompileStatements()
        self.eat()

        if self.tokenizer.current_token == "else":
            self.eat()
            self.eat()
            self.CompileStatements()
            self.eat()


        self.writeCloseTag("ifStatement")

    def CompileWhile(self): # while(expressios){statements}
        self.writeOpenTag("whileStatement")
        
        self.eat()
        self.eat()
        self.CompileExpression()
        self.eat()
        self.eat()
        self.CompileStatements()
        self.eat()

        self.writeCloseTag("whileStatement")


    def CompileReturn(self): #'return' expression? ';'
        self.writeOpenTag("returnStatement")
        
        self.eat()  
        if self.tokenizer.current_token != ";":
            self.CompileExpression()
        self.eat()  
        
        self.writeCloseTag("returnStatement")
    
    def CompileDo(self): #'do' subroutineCall ';'
        
        #subroutineCall:
        #subroutineName '(' expressionList ')'
        #(className | varName) '.' subroutineName '(' expressionList ')'
        
        self.writeOpenTag("doStatement")
        
        self.eat()  
        self.eat()  
        if self.tokenizer.current_token == ".":
            self.eat()  
            self.eat()  
        self.eat()  
        self.CompileExpressionList()
        self.eat()
        self.eat()  
        
        self.writeCloseTag("doStatement")
        

##=========================================================================

    def CompileExpression(self): #grammar: term (op term)*
        
        self.writeOpenTag("expression")
        
        self.CompileTerm()
         
        while self.tokenizer.current_token in {"+","-","*","/","&", "|", "<", ">", "="}:
            self.eat()
            self.CompileTerm()
        
        self.writeCloseTag("expression")



    def CompileTerm(self):

        self.writeOpenTag("term")

        current = self.tokenizer.current_token

        if self.tokenizer.tokenType() == Tokenizer.INT_CONSTANT:
            self.eat() # integer const, e.g 123

        elif self.tokenizer.tokenType() == Tokenizer.STRING_CONSTANT:
            self.eat() # string const, e.g "abc"

        elif current in {"true", "false", "null", "this"}:
            self.eat() # keyword const

        elif current == "(": #e.g.(x+1)
            self.eat()
            self.CompileExpression()
            self.eat()

        elif current == "-" or current == "~":
            self.eat()
            self.CompileTerm()

        elif self.tokenizer.tokenType() == Tokenizer.IDENTIFIER: # there are 3 possibilities when syntax starts with an identifier
            self.eat()

            #Array Access
            if self.tokenizer.current_token == "[": 
                # grammar: varName '[' expression ']' e.g. x[a+1]
                self.eat() # [ 
                self.CompileExpression() # a+1
                self.eat() # ]
            
            #Subroutine Call
            elif self.tokenizer.current_token == "(":
                # grammar: subroutineName '(' expressionList ')'  e.g. foo(x+1)
                self.eat()
                self.CompileExpressionList()
                self.eat()

            #Subroutine Call
            elif self.tokenizer.current_token == ".":  
                # grammar: (className | varName) '.' subroutineName '(' expressionList ')' e.g. Output.printLine(x)
                self.eat()                 
                self.eat()                 
                self.eat()                 
                self.CompileExpressionList()
                self.eat()   

        self.writeCloseTag("term")

    
    def CompileExpressionList(self):
        self.writeOpenTag("expressionList")

        if self.tokenizer.current_token != ")": # if e.g. foo(), then no expression exists
            self.CompileExpression()
            while self.tokenizer.current_token == ",":
                self.eat()  # ,
                self.CompileExpression()
        self.writeCloseTag("expressionList")

##===========================================================================



### Helper Functions:

    def writeLine(self,line): #adds indentation and nextLine for a line
        self.output.write("  "*self.indentation + line + "\n") 
        

    def writeOpenTag(self,tag):
        self.writeLine(f"<{tag}>")
        self.indentation += 1

    def writeCloseTag(self,tag):
        self.indentation -= 1
        self.writeLine(f"</{tag}>")

    def escape(self, value): #escaping for certain symbols
        if value == "<":
            return "&lt;"
        elif value == ">":
            return "&gt;"
        elif value == "&":
            return "&amp;"
        return value
    
    def writeCurrentToken(self): #write the current token in xml format
        tag = self.tokenizer.tokenType()
        value = self.tokenizer.current_token
        value = self.escape(value)
        self.writeLine(f"<{tag}> {value} </{tag}>")    

    def eat(self): # write the xml format for 
    #current token, and move onto the next token
        self.writeCurrentToken()
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
    