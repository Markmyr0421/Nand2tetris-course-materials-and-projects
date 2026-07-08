class SymbolTable:
    STATIC = "static"
    FIELD = "field"
    ARG = "argument"
    VAR = "var"
    #constructor, create a new symbol table
    def __init__(self):
        self.class_scope = {}
        self.subroutine_scope = {}

        self.count = {
            "static": 0,
            "field": 0,
            "argument": 0,
            "var": 0
        }
    
    #Starts a new subroutine scope 
    #(i.e., resets the subroutine's symbol table).
    def startSubroutine(self):
        self.subroutine_scope = {}
        self.count["argument"] = 0
        self.count["var"] = 0

    
    #Defines a new identifier of the given name, 
    #type, and kind, and assigns it a running index.
    def define(self, name, type, kind):
        if kind == "arg":
            kind = "argument"

        index = self.count[kind]
        entry = {
            "type": type,
            "kind": kind,
            "index": index
        }
        if kind in ("static", "field"):
            self.class_scope[name] = entry
        elif kind in ("argument", "var"):
            self.subroutine_scope[name] = entry

        self.count[kind] += 1


    
    #Returns the number of variables of the given kind
    #already defined in the current scope.
    def VarCount(self, kind)->int:
        return self.count[kind]

    #Returns the kind of the named identifier in the current scope.
    #If the identifier is unknown in the current scope, returns NONE.
    def KindOf(self, name):
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]["kind"]
        if name in self.class_scope:
            return self.class_scope[name]["kind"]
        return None


    #Returns the type of the named identifier 
    #in the current scope.
    def TypeOf(self, name)->str:
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]["type"]
        if name in self.class_scope:
            return self.class_scope[name]["type"]
        return None
        

    #Returns the index assigned to the named identifier.
    def IndexOf(self, name)->int:
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]["index"]
        if name in self.class_scope:
            return self.class_scope[name]["index"]
        return None
        