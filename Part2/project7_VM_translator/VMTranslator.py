import os
import sys
import Parser
import CodeWriter

def translate_file(input_file_path, writer):
    writer.setFileName(input_file_path)
    parser = Parser.Parser(input_file_path)

    while parser.hasMoreCommands():
        parser.advance()
        cmd_type = parser.getCmdType()  

        if cmd_type in ["C_PUSH", "C_POP"]:
            arg1 = parser.arg1()
            arg2 = parser.arg2()
            writer.writePushPop(cmd_type, arg1, arg2)    

        elif cmd_type == "C_ARITHMETIC":
            cmd = parser.arg1() 
            writer.writeArithmetic(cmd)

def main():
    if len(sys.argv) != 2:
        print("Usage: python VMTranslator.py <input-file.vm | input-directory>")
        sys.exit(1)
        
    path = sys.argv[1]
    vm_files = []
    output_path = ""

    # 2. 判定输入是单个文件还是文件夹
    if os.path.isfile(path):
        if not path.endswith(".vm"):
            print("Error: File must have a .vm extension")
            sys.exit(1)
        vm_files.append(path)
        # 输出的 .asm 文件与输入文件同名同路径
        output_path = path.replace(".vm", ".asm")
        
    elif os.path.isdir(path):
        # 如果是文件夹，搜集里面所有的 .vm 文件
        for file in os.listdir(path):
            if file.endswith(".vm"):
                vm_files.append(os.path.join(path, file))
        if not vm_files:
            print("Error: No .vm files found in the directory")
            sys.exit(1)
        # 输出的 .asm 文件名等于文件夹的名字，并放在该文件夹内
        dir_name = os.path.basename(os.path.normpath(path))
        output_path = os.path.join(path, f"{dir_name}.asm")
    else:
        print("Error: Invalid path")
        sys.exit(1)

    # 3. 初始化唯一的 CodeWriter
    writer = CodeWriter.CodeWriter(output_path)

    # 4. 依次翻译所有的 .vm 文件
    for vm_file in vm_files:
        print(f"Translating: {vm_file}")
        translate_file(vm_file, writer)
        
    # 5. 必须关闭 writer，确保缓冲区里的汇编代码全部写入硬盘
    writer.close()
    print(f"Success! Output written to: {output_path}")

if __name__ == "__main__":
    main()