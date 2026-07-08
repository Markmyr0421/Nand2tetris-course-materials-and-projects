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
        if self.current_instruction.startswith("push"):
            return "C_PUSH"
        if self.current_instruction.startswith("pop"):
            return "C_POP"
        else:
            return "C_ARITHMETIC"
        
    def arg1(self)->str:
        parts = self.current_instruction.split()
        if self.getCmdType() == "C_ARITHMETIC":
            return parts[0]
        else:
            return parts[1]

    def arg2(self)->int:
        if self.getCmdType() == "C_PUSH" or self.getCmdType() == "C_POP":
            parts = self.current_instruction.split()
            return int(parts[2])
        return None
