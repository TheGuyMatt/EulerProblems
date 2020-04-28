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
faces = '2 3 4 5 6 7 8 9 T J Q K A'
lowaces = 'A 2 3 4 5 6 7 8 9 T J Q K'
face = faces.split()
lowace = lowaces.split()

#creates hand from string and returns a list of "card" objects
def makeHand(cards='4C 3S 6S 7D 5C'):
    hand = []
    for card in cards.split():
        f, s = card[:-1], card[-1]
        assert f in face, f"Error: card face '{f}' does not exist"
        assert s in suit, f"Error: card suit '{s}' does not exist"
        hand.append(Card(f, s))
    assert len(hand) == 5, f"Error: Hand must be 5 cards not {len(hand)}"
    assert len(set(hand)) == 5, f"Error: Hand must have all unique cards {cards}"
    return hand

#checks if hand is a "straight" rank
def straight(hand):
    f, fs = ( (lowace, lowaces) if any(card.face == '2' for card in hand) else (face, faces))
    ordered = sorted(hand, key=lambda card: (f.index(card.face), card.suit))
    if ' '.join(card.face for card in ordered) in fs:
        return 'straight', ordered[-1].face
    return False

#checks if hand is a "threeofakind" rank
def threeofakind(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    if len(allftypes) <= 2:
        return False
    for f in allftypes:
        if allfaces.count(f) == 3:
            allftypes.remove(f)
            return 'threeofakind', [f] + sorted(allftypes, key=lambda f: face.index(f), reverse=True)
    else:
        return False

#checks if hand is a "twopair" rank
def twopair(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    pairs = [f for f in allftypes if allfaces.count(f) == 2]
    if len(pairs) != 2:
        return False
    p0, p1 = pairs
    other = [(allftypes - set(pairs)).pop()]
    return 'twopair', pairs + other if face.index(p0) > face.index(p1) else pairs[::-1] + other

#checks if hand is a "onepair" rank
def onepair(hand):
    allfaces = [f for f, s in hand]
    allftypes = set(allfaces)
    pairs = [f for f in allftypes if allfaces.count(f) == 2]
    if len(pairs) != 1:
        return False
    allftypes.remove(pairs[0])
    return 'onepair', pairs + sorted(allftypes, key=lambda f: face.index(f), reverse=True)

#checks if hand is a "high card" rank
def highcard(hand):
    allfaces = [f for f, s in hand]
    #returns the rank and the cards sorted by value in case of a needed tie breaker
    return 'highcard', sorted(allfaces, key=lambda f: face.index(f), reverse=True)

#gives full file path to poker hands file
script_path = os.path.dirname(__file__)
filename = os.path.join(script_path, "hands.txt")

if __name__ == "__main__":
    #open the file
    with open(filename, "r") as f:
        #loop through file
        for line in f:
            #separate cards into lists representing each "player"
            cards = line.split()
            player_one = [cards[0] + ' ', cards[1] + ' ', cards[2] + ' ', cards[3] + ' ', cards[4]]
            player_two = [cards[5] + ' ', cards[6] + ' ', cards[7] + ' ', cards[8] + ' ', cards[9]]
            #create string variables for the functions to parse
            player_one_str = ''.join(player_one)
            player_two_str = ''.join(player_two)

            #creates hand of the 'card' class
            print(makeHand(player_one_str))
            print(makeHand(player_two_str))

            print(straight(makeHand()))

            break