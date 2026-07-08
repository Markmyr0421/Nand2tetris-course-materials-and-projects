from Tokenizer import Tokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter


class CompilationEngine:
    # Creates a new compilation engine with the given input and output.
    # The next routine called must be compileClass.
    def __init__(self, input_file_path, output_file_path):
        self.tokenizer = Tokenizer(input_file_path)
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(output_file_path)
        self.class_name = None
        self.label_count = 0

    #helpers
    def _advance(self):
        self.tokenizer.advance()

    def _eat(self, expected):
        if self._current_token() != expected:
            raise SyntaxError(f"Expected '{expected}', got '{self._current_token()}'")
        self._advance()
        
    def _current_token(self):
        return self.tokenizer.current_token

    def _peek(self):
        saved_index = self.tokenizer.index
        saved_token = self.tokenizer.current_token
        saved_type = self.tokenizer.token_type

        self.tokenizer.advance()
        next_token = self.tokenizer.current_token

        self.tokenizer.index = saved_index
        self.tokenizer.current_token = saved_token
        self.tokenizer.token_type = saved_type
        return next_token

    def _new_label(self, prefix):
        label = f"{prefix}{self.label_count}"
        self.label_count += 1
        return label

    def _is_type(self):
        token = self._current_token()
        return token in ("int", "char", "boolean") or self.tokenizer.tokenType() == Tokenizer.IDENTIFIER

    # Compiles a complete class.
    def compileClass(self):
        self._advance()
        self._eat("class")
        self.class_name = self._current_token()
        self._advance()
        self._eat("{")

        while self._current_token() in ("static", "field"):
            self.compileClassVarDec()

        while self._current_token() in ("constructor", "function", "method"):
            self.compileSubroutineDec()

        self._eat("}")

    # Compiles a static variable declaration, or a field declaration.
    def compileClassVarDec(self):
        kind = self._current_token()
        self._advance()
        type_name = self._current_token()
        self._advance()

        while True:
            name = self._current_token()
            self.symbol_table.define(name, type_name, kind)
            self._advance()

            if self._current_token() != ",":
                break
            self._eat(",")

        self._eat(";")

    # Compiles a complete method, function, or constructor.
    def compileSubroutineDec(self):
        subroutine_kind = self._current_token()
        self.symbol_table.startSubroutine()
        if subroutine_kind == "method":
            self.symbol_table.define("this", self.class_name, "argument")

        self._advance()
        self._advance()  # return type
        subroutine_name = self._current_token()
        self._advance()

        self._eat("(")
        self.compileParameterList()
        self._eat(")")
        self.compileSubroutineBody(subroutine_kind, subroutine_name)

    # Compiles a possibly empty parameter list
    # Does not handle the enclosing "()"
    def compileParameterList(self):
        if self._current_token() == ")":
            return

        while True:
            type_name = self._current_token()
            self._advance()
            name = self._current_token()
            self.symbol_table.define(name, type_name, "argument")
            self._advance()

            if self._current_token() != ",":
                break
            self._eat(",")

    # Compiles a subroutine's body
    def compileSubroutineBody(self, subroutine_kind, subroutine_name):
        self._eat("{")

        while self._current_token() == "var":
            self.compileVarDec()

        full_name = f"{self.class_name}.{subroutine_name}"
        n_locals = self.symbol_table.VarCount("var")
        self.vm_writer.writeFunction(full_name, n_locals)

        if subroutine_kind == "constructor":
            field_count = self.symbol_table.VarCount("field")
            self.vm_writer.writePush("constant", field_count)
            self.vm_writer.writeCall("Memory.alloc", 1)
            self.vm_writer.writePop("pointer", 0)
        elif subroutine_kind == "method":
            self.vm_writer.writePush("argument", 0)
            self.vm_writer.writePop("pointer", 0)

        self.compileStatements()
        self._eat("}")

    # Compiles a var declaration
    def compileVarDec(self):
        self._eat("var")
        type_name = self._current_token()
        self._advance()

        while True:
            name = self._current_token()
            self.symbol_table.define(name, type_name, "var")
            self._advance()

            if self._current_token() != ",":
                break
            self._eat(",")

        self._eat(";")

    # Compiles a sequence of statements
    # Does not handle the enclosing "{}"
    def compileStatements(self):
        while self._current_token() in ("let", "if", "while", "do", "return"):
            token = self._current_token()
            if token == "let":
                self.compileLet()
            elif token == "if":
                self.compileIf()
            elif token == "while":
                self.compileWhile()
            elif token == "do":
                self.compileDo()
            elif token == "return":
                self.compileReturn()

    # Compiles a let statement
    def compileLet(self):
        self._eat("let")
        name = self._current_token()
        self._advance()

        is_array = False
        if self._current_token() == "[":
            is_array = True
            self._push_var(name)
            self._eat("[")
            self.compileExpression()
            self._eat("]")
            self.vm_writer.writeArithmetic("add")

        self._eat("=")
        self.compileExpression()
        self._eat(";")

        if is_array:
            self.vm_writer.writePop("temp", 0)
            self.vm_writer.writePop("pointer", 1)
            self.vm_writer.writePush("temp", 0)
            self.vm_writer.writePop("that", 0)
        else:
            self._pop_var(name)

    # Compiles an if statement
    def compileIf(self):
        true_label = self._new_label("IF_TRUE")
        false_label = self._new_label("IF_FALSE")
        end_label = self._new_label("IF_END")

        self._eat("if")
        self._eat("(")
        self.compileExpression()
        self._eat(")")

        self.vm_writer.writeIf(true_label)
        self.vm_writer.writeGoto(false_label)
        self.vm_writer.writeLabel(true_label)

        self._eat("{")
        self.compileStatements()
        self._eat("}")

        if self._current_token() == "else":
            self.vm_writer.writeGoto(end_label)
            self.vm_writer.writeLabel(false_label)
            self._eat("else")
            self._eat("{")
            self.compileStatements()
            self._eat("}")
            self.vm_writer.writeLabel(end_label)
        else:
            self.vm_writer.writeLabel(false_label)

    # Compiles a while statement
    def compileWhile(self):
        exp_label = self._new_label("WHILE_EXP")
        end_label = self._new_label("WHILE_END")

        self.vm_writer.writeLabel(exp_label)
        self._eat("while")
        self._eat("(")
        self.compileExpression()
        self._eat(")")
        self.vm_writer.writeArithmetic("not")
        self.vm_writer.writeIf(end_label)

        self._eat("{")
        self.compileStatements()
        self._eat("}")
        self.vm_writer.writeGoto(exp_label)
        self.vm_writer.writeLabel(end_label)

    # Compiles a do statement
    def compileDo(self):
        self._eat("do")
        self._compileSubroutineCall()
        self._eat(";")
        self.vm_writer.writePop("temp", 0)

    # Compiles a return statement
    def compileReturn(self):
        self._eat("return")
        if self._current_token() != ";":
            self.compileExpression()
        else:
            self.vm_writer.writePush("constant", 0)
        self._eat(";")
        self.vm_writer.writeReturn()

    # Compiles an expression
    def compileExpression(self):
        self.compileTerm()

        while self._current_token() in ("+", "-", "*", "/", "&", "|", "<", ">", "="):
            op = self._current_token()
            self._advance()
            self.compileTerm()
            self._write_op(op)

    # Compiles a term
    def compileTerm(self):
        token = self._current_token()
        token_type = self.tokenizer.tokenType()

        #IntegerConstant:
        if token_type == Tokenizer.INT_CONSTANT:
            self.vm_writer.writePush("constant", int(token))
            self._advance()

        elif token_type == Tokenizer.STRING_CONSTANT:
            self.vm_writer.writePush("constant", len(token))
            self.vm_writer.writeCall("String.new", 1)
            for ch in token:
                self.vm_writer.writePush("constant", ord(ch))
                self.vm_writer.writeCall("String.appendChar", 2)
            self._advance()

        #Keywords
        elif token_type == Tokenizer.KEYWORD:
            if token in ("false", "null"):
                self.vm_writer.writePush("constant", 0)
                self._advance()
            elif token == "true":
                self.vm_writer.writePush("constant", 0)
                self.vm_writer.writeArithmetic("not")
                self._advance()
            elif token == "this":
                self.vm_writer.writePush("pointer", 0)
                self._advance()

        #Simple variables
        elif token_type == Tokenizer.IDENTIFIER:
            next_token = self._peek()
            if next_token == "[":
                name = token
                self._push_var(name)
                self._advance()
                self._eat("[")
                self.compileExpression()
                self._eat("]")
                self.vm_writer.writeArithmetic("add")
                self.vm_writer.writePop("pointer", 1)
                self.vm_writer.writePush("that", 0)
            elif next_token in ("(", "."):
                self._compileSubroutineCall()
            else:
                self._push_var(token)
                self._advance()

        #parenthesized expression:  (expression)
        elif token == "(":
            self._eat("(")
            self.compileExpression()
            self._eat(")")
        
        #unary ops:
        elif token in ("-","~"):
            op = token
            self._advance()
            self.compileTerm()

            if op == "-":
                self.vm_writer.writeArithmetic("neg")
            else:
                self.vm_writer.writeArithmetic("not")

        else:
            raise SyntaxError(f"Invalid term: {token}")
    
    #Helper
    def _segment(self, kind):
        if kind == "static":
            return "static"
        if kind == "field":
            return "this"
        if kind == "argument":
            return "argument"
        if kind == "var":
            return "local"
        raise ValueError(f"Unknown kind: {kind}")

    def _push_var(self, name):
        kind = self.symbol_table.KindOf(name)
        index = self.symbol_table.IndexOf(name)
        self.vm_writer.writePush(self._segment(kind), index)

    def _pop_var(self, name):
        kind = self.symbol_table.KindOf(name)
        index = self.symbol_table.IndexOf(name)
        self.vm_writer.writePop(self._segment(kind), index)

    def _write_op(self, op):
        if op == "+":
            self.vm_writer.writeArithmetic("add")
        elif op == "-":
            self.vm_writer.writeArithmetic("sub")
        elif op == "*":
            self.vm_writer.writeCall("Math.multiply", 2)
        elif op == "/":
            self.vm_writer.writeCall("Math.divide", 2)
        elif op == "&":
            self.vm_writer.writeArithmetic("and")
        elif op == "|":
            self.vm_writer.writeArithmetic("or")
        elif op == "<":
            self.vm_writer.writeArithmetic("lt")
        elif op == ">":
            self.vm_writer.writeArithmetic("gt")
        elif op == "=":
            self.vm_writer.writeArithmetic("eq")

    def _compileSubroutineCall(self):
        name = self._current_token()
        self._advance()
        n_args = 0

        if self._current_token() == ".":
            self._eat(".")
            subroutine_name = self._current_token()
            self._advance()

            if self.symbol_table.KindOf(name) is not None:
                self._push_var(name)
                n_args = 1
                full_name = f"{self.symbol_table.TypeOf(name)}.{subroutine_name}"
            else:
                full_name = f"{name}.{subroutine_name}"
        else:
            self.vm_writer.writePush("pointer", 0)
            n_args = 1
            full_name = f"{self.class_name}.{name}"

        self._eat("(")
        n_args += self.compileExpressionList()
        self._eat(")")
        self.vm_writer.writeCall(full_name, n_args)

    # Compiles a possibly empty comma-separated list of expressions
    # Returns the number of expressions in the list
    def compileExpressionList(self):
        n_args = 0
        if self._current_token() == ")":
            return n_args

        while True:
            self.compileExpression()
            n_args += 1

            if self._current_token() != ",":
                break
            self._eat(",")

        return n_args

    # Closes the output VM file
    def close(self):
        self.vm_writer.close()