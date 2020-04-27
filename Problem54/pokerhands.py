#This code finds the full file path.
#VSCode by default needs more than
#the file name to find the correct
#file.
import os.path
scriptpath = os.path.dirname(__file__)
filename = os.path.join(scriptpath, "hands.txt")

#Read from the poker hands file
with open(filename, "r") as f:
    for line in f:
        print(line)