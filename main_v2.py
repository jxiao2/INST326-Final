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
    
    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value


   
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
            
            
class Player: 
    
    def __init__(self, name):
        self.name = name
        # 4 cards in hand
        self.hand = []        
        # 6 personal decks
        self.decks = [[] for _ in range(6)] 
        self.completed_decks = 0

    def swap_with_deck(self, deck_index):
        """Daniel's part: Swap hand with a deck only if
        it's not completed(4 of a kind)."""
        pass

    def has_four_of_a_kind(self):
        """Ryan's part: Check if self.hand is a 4-of-a-kind"""
        pass


# First: __init__ CardGame(): initializes deck, players, and center cards
# Second: deal cards to players and center
# Third: players alternate play_turn: gives option to swap with center or deck
# If choosing first option (center_swap()), player chooses a card 
# from their hand and a card from the center. 
# After swapping with center, check if player has 4 of a kind in hand
# If choosing second option (swap_with_deck()), player chooses a deck to swap with
# At the end of each turn, call check_victory() to see if player has won 

class CardGame:
    def __init__(self, player_names):
        self.deck = Deck()
        self.center_cards = []
        self.deck.shuffle()
        self.deal_cards()
        self.players = [Player(name) for name in player_names]

    def deal_cards(self):
        """Steph's part: Deal cards to players hands/deck, and the center."""
        pass
    
    def center_swap(self, player, player_card, center_card):
        """
        Tanika's part: 
        Swap one card from player's hand with a card from center.

        Args:
            player (Player): the current player
            player_card (Card): the Card object in the player's hand to swap
            center_card (Card): the Card object in the center to swap

        Returns:
            bool:   False if cards requested are invalid, 
                    True if swap is successful.
        """
        if player_card not in player.hand:
            print(f"{player_card} isn't in {player.name}'s hand")
            return False
        else: 
            hand_index = [i for i in range(len(player.hand)) 
                        if player.hand[i] == player_card][0]

        if center_card not in self.center_cards:
            print(f"{center_card} isn't a center card")
            return False
        else:
            center_index = [i for i in range(len(self.center_cards)) 
                            if self.center_cards[i] == center_card][0]

        # Swap cards
        temp = player.hand[hand_index]
        player.hand[hand_index] = self.center_cards[center_index]
        self.center_cards[center_index] = temp

        return True



    def check_victory(self, player):
        """Ryan's part: check if a player has won (player.completed_decks == 6)"""
    pass

    def play_turn(self, player_index):
        """Each turn, player chooses to swap with center or swap deck """
        pass
    
           
def main(args):
    # deck = Deck() -> added this to init of cardGame
    # deck.shuffle()  -> added this to init of cardGame
    game = CardGame(args)
    game.deal_cards()
    
    # each player takes turns until a player wins
    player1 = game.players[0]
    player2 = game.players[1]
    while (not game.check_victory(player1) and 
           not game.check_victory(player2)):
        game.play_turn(0)
        
        game.play_turn(1)


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