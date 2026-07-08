import os
import sys

from CompilationEngine import CompilationEngine


def compile_file(input_path):
    output_path = os.path.splitext(input_path)[0] + ".vm"
    engine = CompilationEngine(input_path, output_path)
    engine.compileClass()
    engine.close()


def main():
    if len(sys.argv) != 2:
        print("Usage: python JackCompiler.py <file.jack | directory>")
        return

    input_path = sys.argv[1]

    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.endswith(".jack"):
                compile_file(os.path.join(input_path, filename))
    elif input_path.endswith(".jack"):
        compile_file(input_path)
    else:
        raise ValueError("Input must be a .jack file or a directory")


if __name__ == "__main__":
    main()
