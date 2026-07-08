// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//// Replace this comment with your code.

//Pseudo code:
//n=R1
//i=1
//result = 0
//LOOP:
//if i>R1 goto STOP
//R2 = R2 + R0
//i ++
//goto LOOP
//R2 = result

    @R1
    D=M
    @n
    M=D
    @i
    M=1
    @result
    M=0

    (LOOP)
    @i
    D=M
    @n
    D=D-M
    @STOP
    D;JGT
    @R0
    D=M
    @result
    M=M+D
    @i
    M=M+1
    @LOOP
    0;JMP

    (STOP)
    @result
    D=M
    @R2
    M=D

    (END)
    @END
    0;JMP

    
//------------------------------
    @R1
    D=M
    @n
    M=D
    @i
    M=1
    @result
    M=0
(LOOP)
    @i
    D=M  
    @n
    D=D-M
    @STOP
    D;JGT
    @R0
    D=M
    @result
    M=M+D
    @i
    M=M+1
    @LOOP
    0;JMP

(STOP)
    @result
    D=M
    @R2
    M=D

(END)
    @END
    0;JMP








