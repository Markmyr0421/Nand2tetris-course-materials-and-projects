class Parser:
    def __init__(self,file_path:str):
        self.instruction = []
        self.current_index = -1
        self.current_instruction = None
        with open(file_path,"r") as file:
            for line in file:
                clean_line = line.split('//')[0].strip()
                if clean_line:
                    self.instruction.append(clean_line)
        
        self.cmdType = None

    def hasMoreCommands(self):
        return (self.current_index +1) < len(self.instruction)

    def advance(self):
        self.current_index += 1
        self.current_instruction = self.instruction[self.current_index]

    def getCmdType(self):
        words = self.current_instruction.strip().split()
        if not words or words[0].startswith("//"):
            return None
        first_word = words[0]
        if first_word.startswith("push"):
            return "C_PUSH"
        if first_word.startswith("pop"):
            return "C_POP"
        if first_word.startswith("goto"):
            return "C_GOTO"
        if first_word.startswith("if-goto"):
            return "C_IF"
        if first_word.startswith("label"):
            return "C_LABEL"
        if first_word.startswith("function"):
            return "C_FUNCTION"
        if first_word.startswith("call"):
            return "C_CALL"
        if first_word.startswith("return"):
            return "C_RETURN"
        else:
            return "C_ARITHMETIC"
        
    def arg1(self)->str:
        parts = self.current_instruction.split()
        cmd_type = self.getCmdType
        if cmd_type() == "C_ARITHMETIC":
            return parts[0]
        if cmd_type() == "C_GOTO":
            return parts[1]
        if cmd_type() == "C_IF":
            return parts[1]
        if cmd_type() == "C_LABEL":
            return parts[1]
        if cmd_type() == "C_FUNCTION":
            return parts[1]
        if cmd_type() == "C_CALL":
            return parts[1]
        if cmd_type() == "C_PUSH" or self.getCmdType() == "C_POP":
            return parts[1]

    def arg2(self)->int:
        if self.getCmdType() == "C_PUSH" or self.getCmdType() == "C_POP":
            parts = self.current_instruction.split()
            return int(parts[2])
        if self.getCmdType() == "C_FUNCTION":
            parts = self.current_instruction.split()
            return int(parts[2])
        if self.getCmdType() == "C_CALL":
            parts = self.current_instruction.split()
            return int(parts[2])

        return "C_RETURN"
