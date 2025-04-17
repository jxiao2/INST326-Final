import argparse
import sys
import random

class Card:
    """A class that descirbes a playing card
    
    Attributes: 
        suit (str): the suit of the card
        value (str): the value of the card
    """
    def __init__(self, suit, value):
        """Initializes a card object with a suit and a value

        Args:
            suit (str): suit of the card
            value (str): value of the card
            
        Side effects: 
            sets the suit of a card to one of the four suits
            sets the value of a card to either 2-10, ace, jack, queen or king
        """
        self.suit = suit
        self.value = value
     
   
class Deck: 
    """A class that describes a deck of 52 playing cards
    
    Attributes: 
        suits (list of str): a list of possible suits for a card
        values (list of str): a list of possible card values
        deck (list of Card): a list of card objects
    """
    def __init__(self):
        """Initializes a deck object with a list of card objects
        
        Side effects: 
            adds 52 card objects to the deck attribute, one for each unique card
        """
        self.suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
        self.values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        
        # Create Deck
        self.deck = [Card(suit, value) for suit in self.suits for value in self.values]
    
    
    def shuffle(self):
        """Shuffles the deck of cards
        
        Side effects: 
            reorders the deck following a riffle style shuffle
        """
        # Shuffle 10-20 times
        for _ in range(10, random.randint(11, 20)):
            cut = len(self.deck) // 2 + random.randint(-5, 5)
            left = self.deck[cut:]
            right = self.deck[:cut]
            self.deck.clear()
            
            while left or right:
                # If both left and right decks have cards, randomly choose one to add back to the deck
                if left and right: 
                    if random.randint(1, 2) == 1:
                        self.deck.append(left.pop())
                    else: 
                        self.deck.append(right.pop())
                # Otherwise, add the card from whichever deck has remaning cards
                elif not left: 
                    self.deck.append(right.pop())
                else: 
                    self.deck.append(left.pop())
            
            
        

def main(args):
    deck = Deck()
    deck.shuffle()

    # Prints shuffled deck    
    # for i in range(len(deck.deck)):
    #     print(f"{deck.deck[i].suit} {deck.deck[i].value}")
    
            
            

def parse_args(arglist):
    """Parse command line arguments
    
    Expect two mandatory arguments: 
        - str: name of player 1
        - str: name of player 2

    Args:
        arglist (list of str): arguments from command line

    Returns:
        namespace: parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("player1", help="Name of player 1")
    parser.add_argument("player2", help="Name of player 2")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)
