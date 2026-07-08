// push constant 10
                @10
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // pop LCL 0

                @LCL
                D=M
                @0
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
                // push constant 21
                @21
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // push constant 22
                @22
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // pop ARG 2

                @ARG
                D=M
                @2
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
                // pop ARG 1

                @ARG
                D=M
                @1
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
                // push constant 36
                @36
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // pop THIS 6

                @THIS
                D=M
                @6
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
                // push constant 42
                @42
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // push constant 45
                @45
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // pop THAT 5

                @THAT
                D=M
                @5
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
                // pop THAT 2

                @THAT
                D=M
                @2
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
                // push constant 510
                @510
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // pop temp 6
                @SP
                M=M-1
                A=M
                D=M
                @11
                M=D
                // push LCL 0
                @LCL
                D=M
                @0
                D=D+A
                A=D
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // push THAT 5
                @THAT
                D=M
                @5
                D=D+A
                A=D
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                 // add
            @SP
            M=M-1
            A=M
            D=M
            A=A-1
            M=D+M
            // push ARG 1
                @ARG
                D=M
                @1
                D=D+A
                A=D
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                 // subtract
            @SP
            M=M-1
            A=M
            D=M
            A=A-1
            M=M-D
            // push THIS 6
                @THIS
                D=M
                @6
                D=D+A
                A=D
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // push THIS 6
                @THIS
                D=M
                @6
                D=D+A
                A=D
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                 // add
            @SP
            M=M-1
            A=M
            D=M
            A=A-1
            M=D+M
             // subtract
            @SP
            M=M-1
            A=M
            D=M
            A=A-1
            M=M-D
            // push temp 6
                @11
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                 // add
            @SP
            M=M-1
            A=M
            D=M
            A=A-1
            M=D+M
            