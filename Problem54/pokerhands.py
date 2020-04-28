#This code finds the full file path.
#VSCode by default needs more than
#the file name to find the correct
#file.
import os.path
script_path = os.path.dirname(__file__)
filename = os.path.join(script_path, "hands.txt")

#Read from the poker hands file
with open(filename, "r") as f:
    for line in f:
        #split the line into separate cards
        cards = line.split()
        #assign correct cards to each "player"
        player_one = [cards[0], cards[1], cards[2], cards[3], cards[4]]
        player_two = [cards[5], cards[6], cards[7], cards[8], cards[9]]
        
        break