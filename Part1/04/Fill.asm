// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the KBD input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.
//SCREEN = 16384
//KBD = 24576

//(LOOP)
//    if KBD>0
//    goto FILL
//    else
//   goto DEFAULT

//(FILL)
//    color = -1
//    address = &SCREEN
//    FILL_LOOP:
//    while address < &KBD:
//    RAM[address] = color
//    address ++

//(DEFAULT)
//    set color to 0

//---------------------------------------------

(LOOP) 
    @KBD
    D=M
    @BLACK
    D;JGT
    @WHITE
    0;JMP

(BLACK)
    @color
    M=-1
    @FILL
    0;JMP

(WHITE)
    @color
    M=0
    @FILL
    0;JMP

(FILL)
    @SCREEN
    D=A
    @address
    M=D

(FILL_LOOP)
    @color
    D=M
    @address
    A=M
    M=D //set the value at address M as "color"

    @address
    M=M+1 //move onto the next memory location

    @address
    D=M 
    @KBD
    D=D-A //check if address has reached the location where KBD starts

    @FILL_LOOP
    D;JLT

    @LOOP
    0;JMP









