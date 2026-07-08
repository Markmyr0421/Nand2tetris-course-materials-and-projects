import sys
import os
from CompilationEngine import CompilationEngine

class Analyzer:
    def __init__(self, input_path):
        self.input_path = input_path

    def analyze(self):
        jack_files = self.getJackFiles()

        for jack_file in jack_files:
            engine = CompilationEngine(jack_file)
            engine.CompileClass() 
    
    def getJackFiles(self):
        if os.path.isfile(self.input_path):
            return [self.input_path]
        
        jack_files = []
        
        for file_name in os.listdir(self.input_path):
            if file_name.endswith(".jack"):
                full_path = os.path.join(self.input_path, file_name)
                jack_files.append(full_path)
        return jack_files   
    



if __name__ == "__main__":
    input_path = sys.argv[1]
    analyzer = Analyzer(input_path)
    analyzer.analyze()