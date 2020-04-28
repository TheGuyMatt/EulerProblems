import os.path
from collections import namedtuple

#create card class
class Card(namedtuple('Card', 'face, suit')):
    def __repr__(self):
        return ''.join(self)

#create list of suits
suit = 'H D C S'.split()
#create list of card faces
#one has to have ace as low value for finding straights
faces = '2 3 4 5 6 7 8 9 10 J Q K A'
lowaces = 'A 2 3 4 5 6 7 8 9 10 J Q K'
face = faces.split()
lowace = lowaces.split()

#gives full file path to poker hands file
script_path = os.path.dirname(__file__)
filename = os.path.join(script_path, "hands.txt")
#script starting point
if __name__ == "__main__":
    #open the file
    with open(filename, "r") as f:
        #loop through file
        for line in f:
            #separate cards into lists representing each "player"
            cards = line.split()
            player_one = [cards[0], cards[1], cards[2], cards[3], cards[4]]
            player_two = [cards[5], cards[6], cards[7], cards[8], cards[9]]

            print(player_one[0])
            break