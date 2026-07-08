class CodeWriter:
    def __init__(self,output_file_path):
        self.output_file = open(output_file_path, "w")
        self.label_counter = 0
        self.return_label_counter = 0
        self.current_function = ""
        
        self.segment_map = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }
    
    def setFileName(self, filename: str):
        import os
        self.filename = os.path.basename(filename).replace(".vm", "")

    def _scopedLabel(self, label: str):
        if self.current_function:
            return f"{self.current_function}${label}"
        return label

    def writeInit(self):
        asm_code = []
        asm_code.append("// --- BOOTSTRAP INIT ---")
        asm_code.append("@256")
        asm_code.append("D=A")
        asm_code.append("@SP")
        asm_code.append("M=D\n")
        for line in asm_code:
            self.output_file.write(line + "\n")
        self.writeCall("Sys.init", 0)
    def writeLabel(self,arg1:str):
        label = self._scopedLabel(arg1)
        assembly = f"""
        ({label})
        """
        self.output_file.write(assembly)
    def writeGoto(self,arg1:str):
        label = self._scopedLabel(arg1)
        assembly = f"""
        @{label}
        0;JMP
        """
        self.output_file.write(assembly)

    def writeIf(self,arg1:str):
        label = self._scopedLabel(arg1)
        assembly = f"""
        @SP
        M=M-1
        A=M
        D=M
        @{label}
        D;JNE
        """
        self.output_file.write(assembly)
    def writeFunction(self,arg1:str,arg2:int):
        self.current_function = arg1
        assembly = f"""
        ({arg1})
        @{arg2}
        D=A
        @R13
        M=D

        ({arg1}$Loop)
        @R13
        D=M
        @{arg1}$EndLoop
        D;JEQ

        @SP
        A=M
        M=0
        @SP
        M=M+1

        @R13
        M=M-1
        @{arg1}$Loop
        0;JMP

        ({arg1}$EndLoop)
        """
        self.output_file.write(assembly)

    def writeCall(self,arg1:str,arg2:int):

        return_label = f"{arg1}$ret.{self.return_label_counter}"
        self.return_label_counter += 1
        assembly = f"""
        @{return_label}
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

        #push the return address onto the stack

        for segment in ["LCL","ARG","THIS","THAT"]:
            assembly += f"""
            @{segment}
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            """
        # push the segments to the saved frame
        
        assembly += f"""
        @SP
        D=M
        @5
        D=D-A
        @{arg2} 
        D=D-A
        @ARG 
        M=D
        """
        # set ARG = SP - 5 - {arg2}

        assembly += f"""
        @SP
        D=M
        @LCL
        M=D
        """
        #set LCL=SP
        assembly += f"""
        @{arg1}
        0;JMP
        """
        # goto where the function starts
        assembly += f"""
        ({return_label})
        """
        # Declare the return address label
        self.output_file.write(assembly)


    def writeReturn(self):
        assembly = f"""
        @LCL
        D=M
        @R13
        M=D //endframe = LCL: store the content in LCL in a temp reg R13
        
        @5
        A=D-A
        D=M
        @R14
        M=D // R14 = *(endframe-5): R14 stores the return address
        
        @SP
        AM=M-1
        D=M
        @ARG
        A=M
        M=D // *ARG = pop(): place return value for caller

        @ARG
        D=M+1
        @SP
        M=D // SP = ARG + 1

        @R13
        D=M
        @1
        A=D-A
        D=M
        @THAT
        M=D //Restore THAT = *(endFrame - 1)

        // Restore THIS = *(endFrame - 2)
        @R13
        D=M
        @2
        A=D-A
        D=M
        @THIS
        M=D

        // Restore ARG = *(endFrame - 3)
        @R13
        D=M
        @3
        A=D-A
        D=M
        @ARG
        M=D

        // Restore LCL = *(endFrame - 4)
        @R13
        D=M
        @4
        A=D-A
        D=M
        @LCL
        M=D

        // goto return address
        @R14
        A=M
        0;JMP
        """
        self.output_file.write(assembly)

    def writePushPop(self,cmd:str,arg1:str,arg2:int):
        if cmd == "C_PUSH":
            if arg1 in self.segment_map:
                arg1 = self.segment_map[arg1]
                assembly = f"""// push {arg1} {arg2}
                @{arg1}
                D=M
                @{arg2}
                D=D+A
                A=D
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                """
                self.output_file.write(assembly)
            elif arg1 == "constant":
                assembly = f"""// push {arg1} {arg2}
                @{arg2}
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
                """
                self.output_file.write(assembly)
            elif arg1 == "static":
                assembly = f"""// push {arg1} {arg2}
                @{self.filename}.{arg2}
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                """
                self.output_file.write(assembly)
            elif arg1 == "temp":
                target_address = 5 +int(arg2)
                assembly = f"""// push {arg1} {arg2}
                @{target_address}
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                """
                self.output_file.write(assembly)
            elif arg1 == "pointer":
                if arg2 == 0:
                    assembly = f"""// push {arg1} {arg2}
                    @THIS
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """

                elif arg2 == 1:
                    assembly = f"""// push {arg1} {arg2}
                    @THAT
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """
                self.output_file.write(assembly)
        elif cmd == "C_POP":
            if arg1 in self.segment_map:
                arg1 = self.segment_map[arg1]
                assembly = f"""// pop {arg1} {arg2}

                @{arg1}
                D=M
                @{arg2}
                D=D+A
                @R13
                M=D
                @SP
                M=M-1
                A=M
                D=M
                @R13
                A=M
                M=D
                """
                self.output_file.write(assembly)
            
            elif arg1 == "static":
                assembly = f"""// pop {arg1} {arg2}
                @SP
                M=M-1
                A=M
                D=M
                @{self.filename}.{arg2}
                M=D
                """
                self.output_file.write(assembly)

            elif arg1 == "temp":
                target_address = 5 +int(arg2)
                assembly = f"""// pop {arg1} {arg2}
                @SP
                M=M-1
                A=M
                D=M
                @{target_address}
                M=D
                """
                self.output_file.write(assembly)

            elif arg1 == "pointer":
                if arg2 == 0:
                    assembly = f"""// pop {arg1} {arg2}
                    @SP
                    M=M-1
                    A=M
                    D=M
                    @THIS
                    M=D
                    """
                elif arg2 == 1:
                    assembly = f"""// pop {arg1} {arg2}
                    @SP
                    M=M-1
                    A=M
                    D=M
                    @THAT
                    M=D
                    """
                self.output_file.write(assembly)


    def writeArithmetic(self,cmd:str):
        if cmd == "add":
            assembly = f""" // add
            @SP
            M=M-1
            A=M
            D=M
            A=A-1
            M=D+M
            """
            self.output_file.write(assembly)
        
        elif cmd == "sub":
            assembly = f""" // subtract
            @SP
            M=M-1
            A=M
            D=M
            A=A-1
            M=M-D
            """
            self.output_file.write(assembly)
        
        elif cmd == "neg":
            assembly = f""" // negate
            @SP
            M=M-1
            A=M
            M=-M
            @SP
            M=M+1
            """
            self.output_file.write(assembly)

        elif cmd == "eq":
            label_true = f"EQ_TRUE_{self.label_counter}"
            label_end = f"EQ_END_{self.label_counter}"
            self.label_counter += 1
            assembly = f""" // check if equal
            @SP
            M=M-1
            A=M
            D=M
            A=A-1
            D=M-D
            
            @SP
            A=M-1
            M=0

            @{label_true}
            D;JEQ
            @{label_end}
            0;JMP

            ({label_true})
            @SP
            A=M-1
            M=-1
            ({label_end})

            """
            self.output_file.write(assembly)
        
        elif cmd == "gt":
            label_true = f"GT_TRUE_{self.label_counter}"
            label_end = f"GT_END_{self.label_counter}"
            self.label_counter += 1
            assembly = f""" // check if greater than
            @SP
            M=M-1
            A=M
            D=M
            A=A-1
            D=M-D 
            
            @SP
            A=M-1
            M=0

            @{label_true}
            D;JGT
            @{label_end}
            0;JMP

            ({label_true})
            @SP
            A=M-1
            M=-1
            ({label_end})

            """
            self.output_file.write(assembly)

        elif cmd == "lt":
            label_true = f"LT_TRUE_{self.label_counter}"
            label_end = f"LT_END_{self.label_counter}"
            self.label_counter += 1
            assembly = f""" // check if less than
            @SP
            M=M-1
            A=M
            D=M
            A=A-1
            D=M-D 
            
            @SP
            A=M-1
            M=0

            @{label_true}
            D;JLT
            @{label_end}
            0;JMP

            ({label_true})
            @SP
            A=M-1
            M=-1
            ({label_end})

            """
            self.output_file.write(assembly)    

        elif cmd == "and":
            assembly = f""" // Bitwise and
            @SP
            M=M-1
            A=M
            D=M
            A=A-1
            M=D&M
            """
            self.output_file.write(assembly)   

        elif cmd == "or":
            assembly = f""" // Bitwise or
            @SP
            M=M-1
            A=M
            D=M
            A=A-1
            M=D|M
            """
            self.output_file.write(assembly)

        elif cmd == "not":
            assembly = f""" // not
            @SP
            A=M-1
            M=!M
            """
            self.output_file.write(assembly)    

    def close(self):
        self.output_file.close()    

            





