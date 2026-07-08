class CodeWriter:
    def __init__(self,output_file_path):
        self.output_file = open(output_file_path, "w")
        self.label_counter = 0
        
        self.segment_map = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT"
        }
    
    def setFileName(self, filename: str):
        import os
        self.filename = os.path.basename(filename).replace(".vm", "")

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

            





