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
        """(Jacky) Initializes a card object with a suit and a value

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
        """(Tanika) a (formal) string representation of the card object
        
        Techniques used:
            f-strings containing expressions
            magic methods other than init
            
        Returns:
            str: a string representation of the card object
        
        """
        return f"{self.value}{self.suit}"
    
    def __eq__(self, other):
        """(Tanika) checks if two card objects are equal
        
        Techniques used:
            magic methods other than init
            
        Args:
            other (Card): another card object
            
        Returns:
            bool: True if the two card objects are equal, False otherwise
        """
        return self.suit == other.suit and self.value == other.value


   
class Deck: 
    """A class that describes a deck of 52 playing cards
    
    Attributes: 
        suits (list of str): a list of possible suits for a card
        values (list of str): a list of possible card values
        deck (list of Card): a list of Card objects
    """
    def __init__(self):
        """(Daniel) Initializes a deck object with a list of card objects
        
        Techniques used:
        - list comprehensions
        
        Side effects: 
            sets the suits to a list of possible suits 
            sets the values to a list of possible card values
            adds 52 card objects to the deck attribute, one for each unique card
        """
        self.suits = ["♠", "♥", "♣", "♦"]
        self.values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        
        # Create Deck
        self.deck = [Card(suit, value) for suit in self.suits for value in self.values]
    
    
    def shuffle(self):
        """(Jacky) Shuffles the deck of cards
        
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
    """A class that describes a player in the game
    Attributes:
        name (str): the name of the player
        swap_deck_moves (int): the number of deck swaps the player has left
        swap_card_moves (int): the number of card swaps the player has left
        completed_decks (int): the number of completed decks the player has
        hand (list of Card): the player's hand of cards
        decks (list of list of Card): the player's decks of cards
        hand_id (int): the id of the deck associated with the player's hand
        deck_ids (list of int): the ids of the decks associated with the player
    
    """
    
    def __init__(self, name):
        """(Steph) Initializes a player object
        
        Args:
            name (str): the name of the player
            
        Side effects:
            sets the name of the player
            sets the number of deck swaps and card swaps to 1
            sets the number of completed decks to 0
            sets the player's hand to an empty list
            sets the player's decks to a list of 5 empty lists
            sets the id of the player's hand to 1
            sets the ids of the player's decks to [2, 3, 4, 5, 6]
            
        Techniques used:
            list comprehensions
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
        """(Jacky) Checks if a deck has 4 cards and they all share the same value.
        
        Args:
            deck (list of Card): a list of card objects
        
        Returns: 
            bool: True if the deck has 4 cards and they all share the same value
                False otherwise
            
        Techniques used:
            set operations
            set comprehensions
        """
        values = {c.value for c in deck}
        return len(deck) == 4 and values.intersection(set(values)) == values

    def update_completed_decks(self):
        """(Tanika) Re‑count how many 4‑of‑a‑kind piles the player has.
        
        Techniques used:
            comprehensions or generator expressions
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
    """A class that describes a card game
    
    Attributes:
        deck (Deck): a deck of cards
        p1 (Player): the first player
        p2 (Player): the second player
        center_cards (list of Card): a list of cards in the center pile
    
    """
    def __init__(self, p1, p2):
        """ (Steph) Initializes a card game object
        
        Args:
            p1 (Player): the first player
            p2 (Player): the second player
            
        Side effects:
            sets the deck to a new deck object
            shuffles the deck
            sets the players to the two player objects
            sets the center cards to an empty list
            
        Techniques used:
            composition of two custom classes
        """
        self.deck = Deck()
        self.deck.shuffle()
        
        self.p1 = p1
        self.p2 = p2
        
        self.center_cards = []

    def deal_cards(self):
        """(Steph) Deals 6 sets of 4 cards to each player (5 in decks, 1 in hand) 
        and 1 set of 4 face-up cards to the center.
        
        Side effects:
            sets the players' decks to 5 sets of 4 cards
            sets the players' hands to 1 set of 4 cards
            sets the center cards to a set of 4 cards
        
        Techniques used:
            list comprehensions
        
        """

        self.p1.decks = [[self.deck.deck.pop() for _ in range(4)] for _ in range(5)]
        self.p2.decks = [[self.deck.deck.pop() for _ in range(4)] for _ in range(5)]
        
        self.p1.hand = [self.deck.deck.pop() for _ in range(4)]
        self.p2.hand = [self.deck.deck.pop() for _ in range(4)]

        self.center_cards = [self.deck.deck.pop() for _ in range(4)]
    
    def center_swap(self, player):
        """(Tanika) Swaps a card from the player's hand with a card
        from the center
        
        Techniques used:
            f-strings containing expressions 
            tuple unpacking (sequence unpacking)

        Args:
            player (Player): the current player

        Side effects: 
            swaps a card from player hand with a card from the center pile
            swaps a card from the center pile with a card from player hand
            May end the game and terminate the program using sys.exit()
            
            
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
        
        temp1, temp2 = (player.hand[handCardIndex-1], self.center_cards[centerCardIndex-1])
        player.hand[handCardIndex-1], self.center_cards[centerCardIndex-1] = (temp2, temp1)

        player.update_completed_decks()
        
        player.update_completed_decks()
        if self.check_victory(player):
            print(f"\n{player.name} wins the game!")
            sys.exit()
            
    def deck_swap(self, player):
        """ (Daniel) Swaps a deck with the player's hand
        Args:
            player (Player): the current player
            
        Side effects:
            swaps a deck with the player's hand
            updates the player's count of completed decks
            
        Techniques used:
            f-strings containing expressions
            list comprehensions
        
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

    def check_victory(self, player):
        """(Ryan)Checks if player meets win conditions (each deck is completed)
        
        Args:
            player (Player): the current player
            
        Returns:    
            bool: True if the player has completed all decks, False otherwise
        
        Techniques used:
            conditional expressions
        
        """
        return True if player.completed_decks == 6 else False
        

    def save_game(self, current_turn, card_swaps, deck_swaps):
        """ (Ryan) Saves the game to a file
        
        Args:
            current_turn (int): the current turn of the game
            card_swaps (int): the number of card swaps left
            deck_swaps (int): the number of deck swaps left
            
        Side effects:
            creates a file with the name entered by the user
            writes the current state of the game to the file
        
        Techniques used:
            with statements
            f-strings containing expressions
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
        """ (Daniel) Displays the current state of the game board
        
        Args:
            player (Player): the current player
            
        Side effects:
            prints the current state of the game board to the console
        
        Techniques used:
            f-strings containing expressions
            conditional expressions
            
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
        """(Jacky) Each turn, player chooses to swap with center or swap deck 
        
        Args:
            player (Player): the current player
            current_turn (int): the current turn of the game
            card_swaps (int): the number of card swaps left
            deck_swaps (int): the number of deck swaps left
            
        Side effects:
            prints the current state of the game board to the console
            allows the player to choose a move
            updates the player's number of card swaps and deck swaps
            may end the game and terminate the program using sys.exit()
            
        Returns:
            int: 0 if the player chooses to end their turn
            
        Techniques used:
            f-strings containing expressions
            optional parameters and/or keyword arguments
        
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
        """(Ryan) Loads data from input file into the CardGame variables.
        
        
        Args:
            filename (str): the name of the file to load
            
        Side effects:
            sets the players' decks to 5 sets of 4 cards
            sets the players' hands to 1 set of 4 cards
            sets the center cards to a set of 4 cards
        
        Raises:
            FileNotFoundError: if the file does not exist
            ValueError: if the file is not a save file
    
        Techniques used:
            with statements
            composition of two custom classes 
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
        """ (Ryan) Loads the current turn from the input file.
        
        Args:
            filename (str): the name of the file to load
            
        Returns:
            int: the current turn of the game
            
        Raises:
            FileNotFoundError: if the file does not exist
            ValueError: if the file is not a save file
        
        
        Techniques used:
            with statements
            f-strings containing expressions
        
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
        """ (Ryan) Loads the number of card swaps and deck swaps from the input file.
        
        Args:
            filename (str): the name of the file to load
            
        Returns:
            tuple: the number of card swaps and deck swaps
            
        Raises:
            FileNotFoundError: if the file does not exist
            ValueError: if the file is not a save file
            
        Techniques used:
            with statements
            f-strings containing expressions    
        
        """
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
    """ (Steph) Loads the players from the input file.
    
    Args:
        filename (str): the name of the file to load
        
    Returns:
        tuple: a tuple containing the two player objects
        
    Raises:
        FileNotFoundError: if the file does not exist
        ValueError: if the file is not a save file
    
    Techniques used
        f-strings containing expressions
        with statements
        composition of two custom classes 
    
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
    """ (Jacky) The main game loop that runs the game.
    
    Args:
        args (namespace): the command line arguments
        status (str): the status of the game ("New Game" or "Load Game")

    Side effects:
        creates a new game or loads a game from a file
        runs the main game loop until one player wins
        may end the game and terminate the program using sys.exit()
    
    Techniques used:
        composition of two custom classes
        sequence unpacking
        
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
    """(Steph) The main function that runs the game.
    
    Args:
        args (namespace): the command line arguments
    
    Side effects:
        prints the main menu to the console
        allows the user to choose to start a new game or load a game
        may end the game and terminate the program using sys.exit()
    
    Techniques used:
        conditional expressions
        

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
        
    game_brain(args, "New Game" if choice == '1' else "Load Game")


def parse_args(arglist):
    """Parse command line arguments
    
    Techniques used:
        the ArgumentParser class from the argparse module
        keyword arguments - used in add_argument() as keyword args

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
