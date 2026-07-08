import sys
from Analyzer import Analyzer


if __name__ == "__main__":
    input_path = sys.argv[1]
    analyzer = Analyzer(input_path)
    analyzer.analyze()
