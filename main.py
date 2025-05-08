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
        """
        Jacky's part:
        
        Initializes a card object with a suit and a value

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
        """
        Techniques used:
        - f-strings containing expressions
        - magic methods other than init
        """
        return f"{self.value}{self.suit}"
    
    def __eq__(self, other):
        """
        Techniques used:
        - magic methods other than init
        - conditional expressions
        """
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
        
        Techniques used:
        - list comprehensions
        
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
                    card = left.pop() if random.randint(1, 2) == 1 else right.pop()
                    self.deck.append(card) 
                
                # Otherwise, add the card from whichever deck has remaning cards
                elif not left: 
                    self.deck.append(right.pop())
                else: 
                    self.deck.append(left.pop())
            
            
class Player: 
    
    def __init__(self, name):
        """
        
        Techniques used:
        - list comprehensions
        """
        self.name = name
        
        self.swap_deck_moves = 1
        self.swap_card_moves = 1
        
        self.completed_decks = 0
        
        self.hand = [] # 4 cards
        self.decks = [[] for _ in range(5)] # 5 sets of 4 cards
        self.hand_id = 1
        self.deck_ids = [2, 3, 4, 5, 6]
            
    def has_four_of_a_kind(self, deck):
        """True iff deck has 4 cards and they all share the same value.
        
        Techniques used:
        - set operations
        """
        # self.completed_decks += 1
        return len(deck) == 4 and len({c.value for c in deck}) == 1

    # def has_four_of_a_kind(self, deck):
    #     """Ryan's part: Check if self.hand is a 4-of-a-kind
    #     """
    #     deck_values = []
    #     four_of_a_kind = False
    #     for card in deck:
    #         deck_values.append(card.value)
    #     if all(x == deck_values[0] for x in deck_values):
    #         four_of_a_kind = True
    #     if deck == self.hand and four_of_a_kind:
    #         self.completed_decks += 1
            

    def update_completed_decks(self):
        """Re‑count how many 4‑of‑a‑kind piles the player has.
        
        Techniques used:
        - comprehensions or generator expressions
        """
        all_piles = [self.hand] + self.decks
        self.completed_decks = sum(1 for pile in all_piles if self.has_four_of_a_kind(pile))
        
        
# First: __init__ CardGame(): initializes deck, players, and center cards
# Second: deal cards to players and center
# Third: players alternate play_turn: gives option to swap with center or deck
# If choosing first option (center_swap()), player chooses a card 
# from their hand and a card from the center. 
# After swapping with center, check if player has 4 of a kind in hand
# If choosing second option (swap_with_deck()), player chooses a deck to swap with
# At the end of each turn, call check_victory() to see if player has won 

class CardGame:
    def __init__(self, p1, p2):
        self.deck = Deck()
        self.deck.shuffle()
        
        self.p1 = p1
        self.p2 = p2
        
        self.center_cards = []

    def deal_cards(self):
        """ Deals 6 sets of 4 cards to each player (5 in decks, 1 in hand) 
        and 1 set of 4 face-up cards to the center.
        
        Techniques used:
        - list comprehensions
        
        
        """

        self.p1.decks = [[self.deck.deck.pop() for _ in range(4)] for _ in range(5)]
        self.p2.decks = [[self.deck.deck.pop() for _ in range(4)] for _ in range(5)]
        
        self.p1.hand = [self.deck.deck.pop() for _ in range(4)]
        self.p2.hand = [self.deck.deck.pop() for _ in range(4)]

        self.center_cards = [self.deck.deck.pop() for _ in range(4)]
    
    def center_swap(self, player):
        """
        Tanika's part: 
        
        Techniques used:
        - f-strings containing expressions 
        
        
        Swap one card from player's hand with a card from center.

        Args:
            player (Player): the current player

        Side effects: 
            swaps a card from player hand with a card from the center pile
        """
        handCardIndex = input("Card in hand (1-4): ")
        while handCardIndex not in ['1', '2', '3', '4']:
            print("Select valid option")
            handCardIndex = input("Card in hand (1-4): ")
        
        centerCardIndex = input("Swap with (1-4): ")
        while centerCardIndex not in ['1', '2', '3', '4']:
            print("Select valid option")
            centerCardIndex = input("Card in hand (1-4): ")

        handCardIndex = int(handCardIndex)
        centerCardIndex = int(centerCardIndex)
        
        # Swap cards
        temp = player.hand[handCardIndex-1]
        player.hand[handCardIndex-1] = self.center_cards[centerCardIndex-1]
        self.center_cards[centerCardIndex-1] = temp

        player.update_completed_decks()
        
        player.update_completed_decks()
        if self.check_victory(player):
            print(f"\n{player.name} wins the game!")
            sys.exit()
            
    def deck_swap(self, player):
        """
        Techniques used:
        - conditional expressions 
        - f-strings containing expressions
        - list comprehensions
        
        """
        ids = [str(id) for id in player.deck_ids]   
        str_ids = ', '.join(ids)
        choice = input(f"Deck to swap with [{str_ids}]: ")

        while (choice not in ids or
            player.has_four_of_a_kind(
                player.decks[player.deck_ids.index(int(choice))])):
            print("Select a valid option")
            choice = input(f"Deck to swap with [{str_ids}]: ")

        deckIndex = player.deck_ids.index(int(choice))

        player.hand, player.decks[deckIndex] = player.decks[deckIndex], player.hand
        player.hand_id, player.deck_ids[deckIndex] = (
            player.deck_ids[deckIndex],
            player.hand_id,
        )

        player.update_completed_decks()
        if self.check_victory(player):
            print(f"\n{player.name} wins the game!")
            sys.exit()

    def check_victory(self, player):
        """Ryan's part: Checks if player meets win conditions (each deck is completed)
        
        Techniques used:
        - conditional expressions
        """
        return True if player.completed_decks == 6 else False
        

    def save_game(self, current_turn, card_swaps, deck_swaps):
        """
        
        Techniques used:
        - with statements
        - f-strings containing expressions
        """
        filename = input("Enter a name for this save: ")
        with open(filename, 'w') as file:
            file.write(f"Player 1: {self.p1.name}\n")
            for deck in self.p1.decks:
                file.write(f"Player 1 Deck: {deck[0]},{deck[1]},{deck[2]},{deck[3]}\n")
            file.write(f"Player 1 Hand: {self.p1.hand[0]},{self.p1.hand[1]},{self.p1.hand[2]},{self.p1.hand[3]}\n")
            file.write(f"Center Cards: {self.center_cards[0]},{self.center_cards[1]},{self.center_cards[2]},{self.center_cards[3]}\n")
            file.write(f"Player 2: {self.p2.name}\n")
            for deck in self.p2.decks:
                file.write(f"Player 2 Deck: {deck[0]},{deck[1]},{deck[2]},{deck[3]}\n")
            file.write(f"Player 2 Hand: {self.p2.hand[0]},{self.p2.hand[1]},{self.p2.hand[2]},{self.p2.hand[3]}\n")
            file.write(f"Current Turn: {current_turn}\n")
            file.write(f"Player Card Swaps: {card_swaps}\n")
            file.write(f"Player Deck Swaps: {deck_swaps}")
    
    def show_board(self, player):
        """
        
        Techniques used:
        - f-strings containing expressions
        - conditional expressions
        """
        
        print("-------------------------------")
        print(f"Center: {self.center_cards}\n")

        # table piles
        for idx, label in enumerate(player.deck_ids):
            suffix = ": DONE" if player.has_four_of_a_kind(player.decks[idx]) else ""
            print(f"[Deck {label}{suffix}]", end=' ')
        print()

        # hand
        hand_suffix = ": DONE" if player.has_four_of_a_kind(player.hand) else ""
        print(f"[Deck {player.hand_id}{hand_suffix}]: {player.hand}")
        print("-------------------------------")

        
    
    def play_turn(self, player, current_turn, card_swaps=1, deck_swaps=1):
        """Each turn, player chooses to swap with center or swap deck 
        
        Techniques used:
        - f-strings containing expressions
        - optional parameters and/or keyword arguments
        
        """
        player.swap_card_moves = card_swaps
        player.swap_deck_moves = deck_swaps
        while player.swap_card_moves == 1 or player.swap_deck_moves == 1:
            print(f"\n{player.name}'s turn")
            
            self.show_board(player)
            
            print(f"1.) Swap Card ({player.swap_card_moves} left)")
            print(f"2.) Swap Deck ({player.swap_deck_moves} left)")
            print(f"3.) End Turn")
            print(f"4.) Save and Quit\n")
            choice = input("Select move: ")
        
            while choice not in ['1', '2', '3', '4']:
                print("Please select a valid option")
                choice = input("Select move: ")
                
            # Player chooses swap card
            if choice == '1':
                if player.swap_card_moves == 0:
                    print("No more card swaps")
                    continue
                
                self.center_swap(player)
                player.swap_card_moves -= 1
            
            # Player chooses swap deck
            elif choice == '2':
                if player.swap_deck_moves == 0:
                    print("No more deck swaps")
                    continue
                
                self.deck_swap(player)
                player.swap_deck_moves -= 1
                
            # Player chooses to end turn
            elif choice == '3':
                print("\n\n\n")
                return 0
            
            # Player chooses to save and quit
            else: 
                self.save_game(current_turn, player.swap_card_moves, 
                               player.swap_deck_moves)
                sys.exit()
            
        self.show_board(player)
        print("\n\n\n")
    
    def load(self, filename):
        """(Ryan)Loads data from input file into the CardGame variables.
        
        - with statements
        - composition of two custom classes 
        """
        try:
            with open(filename, 'r') as file:
                self.center_cards = []
                self.p1.decks = []
                self.p2.decks = []
                for line in file:
                    line = line.strip()
                    if line.startswith("Player 1 Deck: "):
                        deck_str = line.split(": ", 1)[1]
                        deck_cards = []
                        for i in deck_str.split(",", 3):
                            card_value = i[:-1]
                            card_suit = i[-1]
                            card = Card(card_suit, card_value)
                            deck_cards.append(card)
                        self.p1.decks.append(deck_cards)
                    elif line.startswith("Player 2 Deck: "):
                        deck_str = line.split(": ", 1)[1]
                        deck_cards = []
                        for i in deck_str.split(",", 3):
                            card_value = i[:-1]
                            card_suit = i[-1]
                            card = Card(card_suit, card_value)
                            deck_cards.append(card)
                        self.p2.decks.append(deck_cards)
                    elif line.startswith("Player 1 Hand: "):
                        deck_str = line.split(": ", 1)[1]
                        deck_cards = []
                        for i in deck_str.split(",", 3):
                            card_value = i[:-1]
                            card_suit = i[-1]
                            card = Card(card_suit, card_value)
                            self.p1.hand.append(card)
                    elif line.startswith("Player 2 Hand: "):
                        deck_str = line.split(": ", 1)[1]
                        deck_cards = []
                        for i in deck_str.split(",", 3):
                            card_value = i[:-1]
                            card_suit = i[-1]
                            card = Card(card_suit, card_value)
                            self.p2.hand.append(card)
                    elif line.startswith("Center Cards: "):
                        deck_str = line.split(": ", 1)[1]
                        deck_cards = []
                        for i in deck_str.split(",", 3):
                            card_value = i[:-1]
                            card_suit = i[-1]
                            card = Card(card_suit, card_value)
                            self.center_cards.append(card)
        except FileNotFoundError:
            raise FileNotFoundError(f"Save file '{filename}' not found")
        except ValueError:
           raise ValueError(f"{filename} not a save file")

    def load_turn(self, filename):
        
        """
        Techniques used:
        -  with statements
        -  f-strings containing expressions
        
        """
        try:
            with open(filename, 'r') as file:
                for line in file:
                    if line.startswith("Current Turn: "):
                        current_turn = line.split(": ", 1)[1]
        except FileNotFoundError:
            raise FileNotFoundError(f"Save file '{filename}' not found")
        except ValueError:
           raise ValueError(f"{filename} not a save file") 
       
        return int(current_turn)

    def load_swaps(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    if line.startswith("Player Card Swaps: "):
                        card_swaps = int(line.split(": ", 1)[1])
                    elif line.startswith("Player Deck Swaps: "):
                        deck_swaps = int(line.split(": ", 1)[1])
        except FileNotFoundError:
            raise FileNotFoundError(f"Save file '{filename}' not found")
        except ValueError:
           raise ValueError(f"{filename} not a save file") 
       
        return card_swaps, deck_swaps
    
def load_players(filename):
    """
    Techniques used:
    - f-strings containing expressions
    - with statements
    - composition of two custom classes 
    
    """
    try:
        with open(filename, 'r') as file:
            for line in file:
                    line = line.strip()
                    if line.startswith("Player 1: "):
                        p1 = Player(line.split(": ", 1)[1])
                    elif line.startswith("Player 2: "):
                        p2 = Player(line.split(": ", 1)[1])
    except FileNotFoundError:
        raise FileNotFoundError(f"Save file '{filename}' not found")
    except ValueError:
        raise ValueError(f"{filename} not a save file")
    return p1, p2
                
def game_brain(args, status):
    """
    Techniques used:
    - composition of two custom classes —
    - conditional expressions
    """
    currentTurn = 1
    if status == "New Game":
        p1 = Player(args.player1)
        p2 = Player(args.player2)
        game = CardGame(p1, p2)
        game.deal_cards()
        card_swaps = 1
        deck_swaps = 1
    elif status == "Load Game":
        filepath = input("Enter name of save: ")
        p1, p2 = load_players(filepath)
        game = CardGame(p1, p2)
        game.load(filepath)
        currentTurn = game.load_turn(filepath)
        card_swaps, deck_swaps = game.load_swaps(filepath)
    while p1.completed_decks != 6 and p2.completed_decks != 6: 
        if currentTurn == 1: 
            game.play_turn(p1, currentTurn, card_swaps, deck_swaps)
            currentTurn = 0
        else:
            game.play_turn(p2, currentTurn, card_swaps, deck_swaps)
            currentTurn = 1
        card_swaps = 1
        deck_swaps = 1

        
def main(args):
    """
    
    Techniques used:
    - conditional expressions
    - function composition / program control

    """
    print("******(DANIELS FUN CARD GAME)******")
    print("1.) New Game")
    print("2.) Load Game")
    
    choice = input()
    
    while choice not in ['1', '2']:
        print("1.) New Game")
        print("2.) Load Game")
        print("3.) Rules") 
        print("Please select a valid option")
        choice = input()
        
    if choice == '1': 
        game_brain(args, "New Game")
    elif choice == '2': 
        game_brain(args, "Load Game")

def parse_args(arglist):
    """Parse command line arguments
    
    Techniques used:
    - the ArgumentParser class from the argparse module
    - keyword arguments - used in add_argument() as keyword args
    
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
