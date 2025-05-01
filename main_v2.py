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
        return f"{self.value}{self.suit}"
    
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
        self.suits = ["♠", "♥", "♣", "♦"]
        self.values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        
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
        
        self.swap_deck_moves = 1
        self.swap_card_moves = 1
        
        self.completed_decks = 0
        
        self.hand = [] # 4 cards
        self.decks = [[] for _ in range(5)] # 5 sets of 4 cards

    def swap_with_deck(self, deck_swap = False, card_swap = False, 
                      deck_num = None, card_num1 = None, card_num2 = None, 
                      card_swap_deck = None):
        """Daniel's part: Swap hand with a deck only if
        it's not completed(4 of a kind)."""
        
        #Checks if both decks are incomplete, then allows to be swapped
        if self.has_four_of_a_kind(self.hand) is False and (
                self.has_four_of_a_kind(self.decks(deck_num)) is False):
            if deck_swap:
                    self.hand = self.decks(deck_num)
            if card_swap:
                self.hand[card_num1], self.decks[card_swap_deck][card_num2] = (
                self.decks[card_swap_deck][card_num2], self.hand[card_num1])
        else:
            #Gives you a message if one of the decks are complete
            print("""Invalid move: One of 
                the decks you've chosen are already complete""")

    def has_four_of_a_kind(self, deck):
        """Ryan's part: Check if self.hand is a 4-of-a-kind
        """
        deck_values = []
        four_of_a_kind = False
        for card in deck:
            deck_values.append(card.value)
        if all(x == deck_values[0] for x in deck_values):
            four_of_a_kind = True
        if deck == self.hand and four_of_a_kind:
            self.completed_decks += 1

# First: __init__ CardGame(): initializes deck, players, and center cards
# Second: deal cards to players and center
# Third: players alternate play_turn: gives option to swap with center or deck
# If choosing first option (center_swap()), player chooses a card 
# from their hand and a card from the center. 
# After swapping with center, check if player has 4 of a kind in hand
# If choosing second option (swap_with_deck()), player chooses a deck to swap with
# At the end of each turn, call check_victory() to see if player has won 

class CardGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        
        self.center_cards = []

    def deal_cards(self, p1, p2):
        """ Deals 6 sets of 4 cards to each player (5 in decks, 1 in hand) 
        and 1 set of 4 face-up cards to the center."""

        p1.decks = [[self.deck.deck.pop() for _ in range(4)] for _ in range(5)]
        p2.decks = [[self.deck.deck.pop() for _ in range(4)] for _ in range(5)]
        
        p1.hand = [self.deck.deck.pop() for _ in range(4)]
        p2.hand = [self.deck.deck.pop() for _ in range(4)]

        self.center_cards = [self.deck.deck.pop() for _ in range(4)]
    
    def center_swap(self, player):
        """
        Tanika's part: 
        Swap one card from player's hand with a card from center.

        Args:
            player (Player): the current player

        Side effects: 
            swaps a card from player hand with a card from the center pile
        """
        handCard = input("Card in hand (1-4): ")
        while handCard not in ['1', '2', '3', '4']:
            print("Select valid option")
            handCard = input("Card in hand (1-4): ")
        
        centerCard = input("Swap with (1-4): ")
        while centerCard not in ['1', '2', '3', '4']:
            print("Select valid option")
            centerCard = input("Card in hand (1-4): ")

        handCard = int(handCard)
        centerCard = int(centerCard)
        
        # Swap cards
        temp = player.hand[handCard-1]
        player.hand[handCard-1] = self.center_cards[centerCard-1]
        self.center_cards[centerCard-1] = temp


    def check_victory(self, player):
        """Ryan's part: Checks if player meets win conditions (each deck is completed)
        """
        True if player.completed_decks == 6 else False

    def save(self):
        """(Ryan)Creates a GameState object and calls its save_file method.
        """
        game_state = GameState(self.players, self.deck, self.center_cards)
        game_state.save_file()
    
    def show_board(self, player):
        print("-------------------------------")
        print(f"Center: {self.center_cards}\n")
        
        for i in range(5):
            print(f"[Deck {i+1}]", end=' ')
        
        print(f"\n{player.hand}")
        print("-------------------------------")
        
    
    def play_turn(self, player):
        """Each turn, player chooses to swap with center or swap deck """
        while player.swap_card_moves == 1 or player.swap_deck_moves == 1:
            self.show_board(player)
            
            print(f"\n{player.name}s turn")
            print(f"1.) Swap Card ({player.swap_card_moves} left)")
            print(f"2.) Swap Deck ({player.swap_deck_moves} left)")
            print(f"3.) End Turn")
            print(f"4.) Save and Quit\n")
            choice = input("Select move: ")
        
            while choice not in ['1', '2', '3', '4']:
                print("Please select a valid option")
                choice = input("Select move: ")
                
                
            if choice == '1':
                if player.swap_card_moves == 0:
                    print("No more card swaps")
                    continue
                self.center_swap(player)
                player.swap_card_moves -= 1
            elif choice == '2':
                # Swap deck functionality goes here
                pass
            elif choice == '3':
                # End turn functionality goes here
                pass
            else: 
                # Call save function + quit game here
                pass
    
    def load(self, filename):
        """(Ryan)Loads data from input file into the CardGame variables.
        """
        try:
            with open(filename, 'r') as file:
                self.players = []
                self.center_cards = []
                self.deck = 0
                for line in file:
                    line = line.strip()
                    if line.startswith("Player 1: "):
                        player1 = Player(line.split(": ", 1)[1])
                        self.players.append(player1)
                    elif line.startswith("Player 2: "):
                        player2 = Player(line.split(": ", 1)[1])
                        self.players.append(player2)
                    elif line.startswith("Player 1 Deck: "):
                        deck_str = line.split(": ", 1)[1]
                        deck_cards = []
                        for i in deck_str.split(",", 3):
                            card_value, card_suit = i.split(" of ")[0]
                            card = Card(card_suit, card_value)
                            deck_cards.append(card)
                        self.players[0].decks.append(deck_cards)
                    elif line.startswith("Player 2 Deck: "):
                        deck_str = line.split(": ", 1)[1]
                        deck_cards = []
                        for i in deck_str.split(",", 3):
                            card_value, card_suit = i.split(" of ")[0]
                            card = Card(card_suit, card_value)
                            deck_cards.append(card)
                        self.players[1].decks.append(deck_cards)
                    elif line.startswith("Player 1 Hand: "):
                        deck_str = line.split(": ", 1)[1]
                        deck_cards = []
                        for i in deck_str.split(",", 3):
                            card_value, card_suit = i.split(" of ")[0]
                            card = Card(card_suit, card_value)
                            self.players[0].hand.append(card)
                    elif line.startswith("Player 2 Hand: "):
                        deck_str = line.split(": ", 1)[1]
                        deck_cards = []
                        for i in deck_str.split(",", 3):
                            card_value, card_suit = i.split(" of ")[0]
                            card = Card(card_suit, card_value)
                            self.players[1].hand.append(card)
                    elif line.startswith("Center Cards: "):
                        deck_str = line.split(": ", 1)[1]
                        deck_cards = []
                        for i in deck_str.split(",", 3):
                            card_value, card_suit = i.split(" of ")[0]
                            card = Card(card_suit, card_value)
                            self.center_cards.append(card)
                    elif line.startswith("Card: "):
                        deck_str = line.split(": ", 1)[1]
                        card_value, card_suit = i.split(" of ")[0]
                        card = Card(card_suit, card_value)
                        self.deck.append(card)
        except FileNotFoundError:
            raise FileNotFoundError(f"Save file '{filename}' not found")

class GameState:
    def __init__(self, players, deck, center_cards):
        self.players = players
        self.deck = deck
        self.center_cards = center_cards
    
    def save_file(self, filename):
        """(Ryan)Writes import game data to .txt file
        """
        with open(filename, 'w') as file:
            file.write(f"Player 1: {self.players[0]}")
            for deck in self.players[0].decks:
                file.write(f"Player 1 Deck: {deck[0]},{deck[1]},{deck[2]},{deck[3]}")
            file.write(f"Player 1 Hand: {self.players[0].hand[0]},{self.players[0].hand[1]},{self.players[0].hand[2]},{self.players[0].hand[3]}")
            file.write(f"Center Cards: {self.center_cards[0]},{self.center_cards[1]},{self.center_cards[2]},{self.center_cards[3]},")
            file.write(f"Player 2: {self.players[1]}")
            for deck in self.players[1].decks:
                file.write(f"Player 2 Deck: {deck[0]},{deck[1]},{deck[2]},{deck[3]}")
            file.write(f"Player 2 Hand: {self.players[1].hand[0]},{self.players[1].hand[1]},{self.players[1].hand[2]},{self.players[1].hand[3]}")
            for card in self.deck:
                file.write(f"Card: {card}")
    
def game_brain(args):
    currentTurn = 1
    
    p1 = Player(args.player1)
    p2 = Player(args.player2)
    game = CardGame()
    game.deal_cards(p1, p2)

    while p1.completed_decks != 6 and p2.completed_decks != 6: 
        if currentTurn == 1: 
            game.play_turn(p1)
            currentTurn = 0
        else: 
            game.play_turn(p2)
            currentTurn = 1

        
def main(args):
    print("******(DANIELS FUN CARD GAME)******")
    print("1.) New Game")
    print("2.) Load Game")
    print("3.) Rules") # Might remove and just have a text file in the repo with rules
    
    choice = input()
    
    while choice not in ['1', '2', '3']:
        print("1.) New Game")
        print("2.) Load Game")
        print("3.) Rules") 
        print("Please select a valid option")
        choice = input()
        
    if choice == '1': 
        game_brain(args)
    elif choice == '2': 
        # Load game functionality goes here
        pass
    elif choice == '3': 
        # Display rules here (Make a function for this)
        pass

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
