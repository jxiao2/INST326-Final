# Daniel's Fun Card Game

## Overview

Daniel's Fun Card Game is a card game where two players compete against each other to 
make 6 decks of four-of-a-kind cards first. Players take turns swapping cards with a card in the center, or swapping their current hand with one of their 6 decks.
The first player to complete all six four-of-a-kinds wins!

## How to play: 
The center is the pile both players can access at any time

On your turn you will be displayed your 5 hidden decks, and your hand of 4 cards. 

You have the opportunity to swap a card from your hand with a card in the center. When doing so you will be prompted to choose the card in your hand you wish to swap and a card from the center to be swapped with.

You also have the opportunity to swap your hand with one of your 5 face down decks.

When a 4 of a kind is achieved that deck when placed facedown will be inaccessible and the player gains one point. 

Players take turns until one player achieves 6 points. 

---

## File Descriptions

| File Name         | Purpose                                                                 |
|------------------|-------------------------------------------------------------------------|
| `main.py`         | Main python file with all class & function definitions |
| `README.md`       | Documentation of our python card game|
| `example.txt`     | Example file load of a game   |
| `finished.txt`    | An example file load of a game to simulate a victory   |

---

## How to Run the Program
1: Clone the repository using
```bash
git clone https://github.com/jxiao2/INST326-Final.git
```
2: Run the program using:
```bash
python3 main.py PLAYER1_NAME PLAYER2_NAME
```


## Attribution Table
| Method/Function                 | Primary Author | Techniques Demonstrated                          |
|--------------------------------|----------------|--------------------------------------------------|
| Deck.__init__                  | Daniel         |                                                  |
| CardGame.__init__              | Daniel         |                                                  |
| CardGame.deck_swap             | Daniel         |                                                  |
| CardGame.play_turn             | Daniel         | Optional parameters / keyword arguments          |
| game_brain                     | Daniel         | Sequence unpacking                               |
| Card.__init__                  | Jacky          |                                                  |
| CardGame.show_board            | Jacky          |                                                  |
| Deck.shuffle                   | Jacky          | Conditional expressions                          |
| parse_args                     | Jacky          | ArgumentParser class                             |
| Player.__init__                | Steph          |                                                  |
| CardGame.deal_cards            | Steph          |                                                  |
| main                           | Steph          |                                                  |
| Player.has_four_of_a_kind      | Steph          | Set operations                                   |
| Card.__repr__                  | Steph          | Magic methods (other than __init__)              |
| Player.update_completed_decks  | Tanika         | Generator expressions                            |
| CardGame.center_swap           | Tanika         | f-strings                                         |
| Card.__eq__                    | Tanika         |                                                  |
| CardGame.check_victory         | Tanika         |                                                  |
| CardGame.save_game             | Ryan           | With statements                                  |
| CardGame.load                  | Ryan           | Composition of two custom classes                |
| CardGame.load_turn             | Ryan           |                                                  |
| CardGame.load_swaps            | Ryan           |                                                  |
| load_players                   | Ryan           |                                                  |
