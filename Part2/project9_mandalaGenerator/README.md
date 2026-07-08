# Mandala Generator

Mandala Generator is a drawing program designed by the author for the assignment project09 of nand2tetris course part2.
The program is written in Jack language and compiled using a jack compiler provided by the course.
The user can control a cursor on a centered `256 x 256` canvas and creates
kaleidoscope-style drawings using 8-way symmetry.

## Features

- Centered canvas with logical origin at `(0, 0)`
- 8-way symmetric mandala drawing
- Black and white drawing modes
- Move-only mode for repositioning the cursor
- Visible `+` shaped cursor
- Current cursor coordinate display
- Pixel-by-pixel undo and redo
- Clear canvas command
- Welcome page and instruction page
- Continuous movement when a key is held

## How Symmetry Works

When the user draws at logical coordinate `(x, y)`, the program also draws at
the seven reflected or rotated positions:

```text
(x, y)
(-x, y)
(x, -y)
(-x, -y)
(y, x)
(-y, x)
(y, -x)
(-y, -x)
```

This creates a mandala or kaleidoscope effect from simple cursor movement.

## Controls

### Movement

```text
R : move up
D : move left
F : move down
G : move right

E : move up-left
T : move up-right
X : move down-left
B : move down-right
```

### Drawing

```text
0 : draw mode off, cursor only moves
1 : draw mode on
2 : set color black
3 : set color white / eraser
```

### Canvas History

```text
C : clear canvas
Z : undo one pixel
Y : redo one pixel
```

## How To Run

Since it is a nand2tetris project, you have to first download the software suite on https://www.nand2tetris.org -> Software -> Nand to Tetris Software package:

After downloading,Compile the Jack files:

```bash
cd ~/Desktop/nand2tetris_Project09
~/Desktop/nand2tetris/tools/JackCompiler.sh .
```

Then, open the VM Emulator:

```bash
~/Desktop/nand2tetris/tools/VMEmulator.sh
```

Then load the whole project folder:

```text
/Users/mayouran/Desktop/nand2tetris_Project09
```

Do not load a single `.jack` or `.vm` file. The VM Emulator should load all
compiled `.vm` files in the folder.

After the welcome page appears, press `Space` to start.

## Submission Format

This project follows the nand2tetris Project 09 submission format:

```text
nand2tetris_Project09/
├── Main.vm
├── Drawer.vm
├── History.vm
├── InitiationUI.vm
├── README.md
└── source/
    ├── Main.jack
    ├── Drawer.jack
    ├── History.jack
    └── InitiationUI.jack
```

The root folder contains the compiled VM files used by the VM Emulator. The
`source/` folder contains all Jack source files for code review.

## Source File Structure

```text
source/Main.jack          Control layer. Handles keyboard input, cursor
                          movement, draw mode, symmetry drawing, clear,
                          undo, and redo.

source/Drawer.jack        UI drawing layer. Draws pixels, reads pixels,
                          manages the cursor, clears the canvas, and draws
                          the border.

source/History.jack       Data layer. Stores cursor position, current color,
                          draw mode, and undo/redo stacks.

source/InitiationUI.jack  Start page and instruction screen.
```

## Coordinate System

The Hack screen is `512 x 256`, with origin at the top-left corner. This
program uses a centered `256 x 256` canvas with logical coordinates:

```text
x: -128 to 127
y: -128 to 127
```

`Drawer.jack` converts logical canvas coordinates into Hack screen coordinates
before writing to screen memory.

## Implementation Notes

The Hack screen is black and white only. Each screen memory word stores 16
horizontal pixels. To draw one pixel, the program finds the correct screen
memory word and changes only the target bit.

Undo and redo are implemented with two stacks. Each pixel record stores:

```text
x
y
oldColor
newColor
```

Undo restores `oldColor`; redo restores `newColor`.

## Limitations of the program

- The Hack screen only supports black and white.
- Undo and redo work pixel by pixel, so one symmetric drawing action may need
  several undo or redo presses.
- The visible border uses the outer canvas pixels, so the practical drawing area
  is slightly smaller than the full `256 x 256` canvas.
- can only control the cursor using keyboard instead of other peripheral devices like the mouse.

## Your first Art Piece: A Mandala flower

- After entering draw mode and set color to black, follow the instructions below:
- starts from (0,0)
- Hold R for 15 steps
- Hold T for 8 steps
- Hold F for 15 steps
- Hold X for 8 steps
- Hold R for 5
- Hold E for 5
- Hold F for 5
- Hold B for 5
- press 0 to turn drawMode off
- move the cursor to (35,0)
- press 1 to turn drawMode on
- Hold T for 10
- Hold R for 8
- Hold E for 10
- Hold D for 8
- Hold X for 10
- Hold F for 8
- Hold B for 10
- Hold G for 8

- Then goto (8,4),drawMode off
- turn on draw Mode
- Hold T for 4
- Hold F for 4
- Hold X for 4
- Hold R for 4

And a simple Mandala flower is done!!!