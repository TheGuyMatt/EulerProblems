import os.path

scriptpath = os.path.dirname(__file__)
filename = os.path.join(scriptpath, "hands.txt")

with open(filename, "r") as f:
    for line in f:
        print(line)