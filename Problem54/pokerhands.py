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

#checks if hand is a "straightflush" rank
def straightflush(hand):
    #use different order of faces if the face '2' is used
    f, fs = ((lowace, lowaces) if any(card.face == '2' for card in hand) else (face, faces))
    #order the faces
    ordered = sorted(hand, key=lambda card: (f.index(card.face), card.suit))
    first, rest = ordered[0], ordered[1:]
    #checks if it is actucally a straight flush
    #returns the rank and highest card of straight
    if (all(card.suit == first.suit for card in rest) and ' '.join(card.face for card in ordered) in fs):
        return 8, ordered[-1].face
    return False

#checks if hand is a "fourofakind" rank
def fourofakind(hand):
    #identify all the faces in hand
    allfaces = [f for f, s in hand]
    #identify all the types of faces
    allftypes = set(allfaces)
    #checks if 4 of a kind is possible
    if len(allftypes) != 2:
        return False
    for f in allftypes:
        #checks for the face that is on the 4 cards
        if allfaces.count(f) == 4:
            allftypes.remove(f)
            #returns rank, 4 of a kind face, and the "kicker" card
            return 7, [f, allftypes.pop()]
    else:
        return False

#checks if hand is a "fullhouse" rank
def fullhouse(hand):
    #identify all the faces in hand
    allfaces = [f for f, s in hand]
    #identify all the types of faces
    allftypes = set(allfaces)
    #checks if full house is possible
    if len(allftypes) != 2:
        return False
    for f in allftypes:
        #finds the face that has 3 cards in the full house hand
        if allfaces.count(f) == 3:
            allftypes.remove(f)
            #returns rank and the full house card faces
            return 6, [f, allftypes.pop()]
    else:
        return False

#checks if hand is a "flush" rank
def flush(hand):
    #identify all suit types
    allstypes = {s for f, s in hand}
    #check for flush
    if len(allstypes) == 1:
        #identify all the card faces
        allfaces = [f for f, s in hand]
        #return rank and sorted card faces
        return 5, sorted(allfaces, key=lambda f: face.index(f), reverse=True)
    else:
        return False

#checks if hand is a "straight" rank
def straight(hand):
    #use different order of faces if the face '2' is used
    f, fs = ( (lowace, lowaces) if any(card.face == '2' for card in hand) else (face, faces))
    #order the faces
    ordered = sorted(hand, key=lambda card: (f.index(card.face), card.suit))
    #checks if order is correct for a straight hand
    if ' '.join(card.face for card in ordered) in fs:
        #returns rank and highest card of straight
        return 4, ordered[-1].face
    return False

#checks if hand is a "threeofakind" rank
def threeofakind(hand):
    #identify all card faces in hand
    allfaces = [f for f, s in hand]
    #identify all types of faces in hand
    allftypes = set(allfaces)
    #checks if three of a kind is possible
    if len(allftypes) <= 2:
        return False
    for f in allftypes:
        #finds three of a kind
        if allfaces.count(f) == 3:
            allftypes.remove(f)
            #returns rank, the three of a kind card, and the two "kickers" of the hand
            return 3, [f] + sorted(allftypes, key=lambda f: face.index(f), reverse=True)
    else:
        return False

#checks if hand is a "twopair" rank
def twopair(hand):
    #identify all card faces in hand
    allfaces = [f for f, s in hand]
    #identify all types of faces in hand
    allftypes = set(allfaces)
    #identify all pairs
    pairs = [f for f in allftypes if allfaces.count(f) == 2]
    #checks if there are two pairs
    if len(pairs) != 2:
        return False
    #separates the two pairs
    p0, p1 = pairs
    #finds the other card
    other = [(allftypes - set(pairs)).pop()]
    #returns rank, the two pair faces, and the "kicker" card
    return 2, pairs + other if face.index(p0) > face.index(p1) else pairs[::-1] + other

#checks if hand is a "onepair" rank
def onepair(hand):
    #identify all card faces in hand
    allfaces = [f for f, s in hand]
    #identify all types of faces in hand
    allftypes = set(allfaces)
    #identify all pairs
    pairs = [f for f in allftypes if allfaces.count(f) == 2]
    #checks for the one pair
    if len(pairs) != 1:
        return False
    #separates pair from other faces in hand
    allftypes.remove(pairs[0])
    #returns rank, the pair face, and each face of the "kicker" cards
    return 1, pairs + sorted(allftypes, key=lambda f: face.index(f), reverse=True)

#checks if hand is a "high card" rank
def highcard(hand):
    #identify all card faces in hand
    allfaces = [f for f, s in hand]
    #returns the rank and the card faces in order
    return 0, sorted(allfaces, key=lambda f: face.index(f), reverse=True)

#creates hand from string and returns a list of "card" objects
#goes to default hand in case no hand provided
def makeHand(cards='7C 8C 9C TC JC'):
    hand = []
    for card in cards.split():
        #finds face and suit of card
        f, s = card[:-1], card[-1]
        #checks to make sure face and suit exist
        assert f in face, f"Error: card face '{f}' does not exist"
        assert s in suit, f"Error: card suit '{s}' does not exist"
        #adds card to hand
        hand.append(Card(f, s))
    #checks to make sure that the hand is 5 cards and that each card is unique
    assert len(hand) == 5, f"Error: Hand must be 5 cards not {len(hand)}"
    assert len(set(hand)) == 5, f"Error: Hand must have all unique cards {cards}"
    #returns the hand of 5 cards
    return hand

#determines the order of hands
rankorder = (straightflush, fourofakind, fullhouse, flush, straight, threeofakind, twopair, onepair, highcard)

#function that determines hand rank
def rank(cards):
    #calls makeHand function to turn string into a list of card objects
    hand = makeHand(cards)
    #loop that checks each hand rank function in order
    for ranker in rankorder:
        rank = ranker(hand)
        #checks if it found the rank
        if rank:
            break
    #makes sure the cards could be ranked
    assert rank, f'Error: Can not rank cards: {cards}'
    #return the rank of the hand
    return rank

#decides the winner given two players hands as strings
#returns true for player one, false for player two
def decidewinner(one_player, two_player):
    #finds the two players ranks
    ponerank = rank(one_player)
    ptworank = rank(two_player)
    #tries to compare hands
    if ponerank[0] > ptworank[0]: return True
    elif ponerank[0] < ptworank[0]: return False
    #if the same hand, check the kicker cards
    elif ponerank[0] == ptworank[0]:
        #if the hand is a straight, only need to check the
        #second part of rank as it does not return a list
        if ponerank[0] == 4 or ponerank[0] == 8:
            if face.index(ponerank[1]) > face.index(ptworank[1]): return True
            elif face.index(ponerank[1]) < face.index(ptworank[1]): return False

        #checks "kicker" cards until winner is declared
        for i in range(len(ponerank[1])):
            if face.index(ponerank[1][i]) > face.index(ptworank[1][i]): return True
            elif face.index(ponerank[1][i]) < face.index(ptworank[1][i]): return False

        #if hands can not be ranked pass an error
        raise ValueError('Error: winner could not be decided')
    #if hands can not be ranked pass an error
    else: raise ValueError('Error: winner could not be decided')

#gives full file path to poker hands file
script_path = os.path.dirname(__file__)
#adds the file to the full path
filename = os.path.join(script_path, "hands.txt")

#keeps track of player one's wins
playeronewins = 0

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

            #checks winner
            #increments the "playeronewins" variable
            #to see how many times player one wins
            if (decidewinner(player_one_str, player_two_str)):
                playeronewins += 1
                print('player one wins')
            else:
                print('player two wins')
    print(playeronewins)