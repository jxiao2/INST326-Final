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
    def __init__(self, player1, player2):
        self.deck = Deck()
        self.deck.shuffle()
        
        self.center_cards = []
        self.players = [Player(player1), Player(player2)]

    def deal_cards(self):
        """ Deals 6 sets of 4 cards to each player (5 in decks, 1 in hand) 
        and 1 set of 4 face-up cards to the center."""
        total_cards_needed = (6 * 4 * 2) + 4 
        
        if len(self.deck.deck) < total_cards_needed:
            raise ValueError("Not enough cards in the deck to deal.")
    
        for player in self.players:
            # deal 5 face-down sets 
            for i in range(5):
                player.decks[i] = [self.deck.deck.pop() for _ in range(4)]
    
            # deal 1 hand set 
            player.hand = [self.deck.deck.pop() for _ in range(4)]
            player.decks[5] = player.hand 
       
        self.center_cards = [self.deck.deck.pop() for _ in range(4)]
    
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
        """Ryan's part: Checks if player meets win conditions (each deck is completed)
        """
        True if player.completed_decks == 6 else False

    def play_turn(self, player_index):
        """Each turn, player chooses to swap with center or swap deck """
        pass
    def save(self):
        """(Ryan)Creates a GameState object and calls its save_file method.
        """
        game_state = GameState(self.players, self.deck, self.center_cards)
        game_state.save_file()
    
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
    
           
# def main(args):
#     # deck = Deck() -> added this to init of cardGame
#     # deck.shuffle()  -> added this to init of cardGame
#     game = CardGame(args.player1, args.player2)
#     game.deal_cards()
    
#     # each player takes turns until a player wins
#     player1 = game.players[0]
#     player2 = game.players[1]
#     while (not game.check_victory(player1) and 
#            not game.check_victory(player2)):
#         game.play_turn(0)
        
#         game.play_turn(1)
        
def main(args):
    game = CardGame(args.player1, args.player2)
    print(game)


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
