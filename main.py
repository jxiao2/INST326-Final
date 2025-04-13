import argparse
import sys
import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
class Deck: 
    def __init__(self):
        self.suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
        self.values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        
        # Create Deck
        self.deck = [Card(suit, value) for suit in self.suits for value in self.values]
    
    # Simulate riffle shuffle
    def shuffle(self):
        for _ in range(10, random.randint(11, 20)):
            cut = len(self.deck) // 2 + random.randint(-5, 5)
            left = self.deck[cut:]
            right = self.deck[:cut]
            self.deck.clear()
            
            while left or right:
                if left and right: 
                    if random.randint(1, 2) == 1:
                        self.deck.append(left.pop())
                    else: 
                        self.deck.append(right.pop())
                elif not left: 
                    self.deck.append(right.pop())
                else: 
                    self.deck.append(left.pop())
            
            
        

def main(args):
    deck = Deck()
    deck.shuffle()
    
    # print shuffled deck
    # for i in range(len(deck.deck)):
    #     print(f"{deck.deck[i].suit} {deck.deck[i].value}")
    
            
            

def parse_args(arglist):
    parser = argparse.ArgumentParser()
    parser.add_argument("player1", help="Name of player 1")
    parser.add_argument("player2", help="Name of player 2")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)