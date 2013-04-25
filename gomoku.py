#Main Class
#Gomoku Type Games - Lingliang Zhang / Comp Sci Assignment 4

from player import Player
from ai import AI
from game import Game
import random

def main():
    game = Game()
    player1 = game.player1
    player2 = game.player2


    #AI Learning
    if game.mode  == 1:
        speed = input("""\n%s
Choose a learning mode:
1. Full Mode - Watch the AI learn by playing move by move
(good for understanding the AI and its development)
2. Fast Mode - The AI will hide its moves and only show end-states (faster)
3. Quick-learn - The AI will learn without displaying any output (fastest)
4. Skip - The AI will resort to default intelligence values (no learning)

(1 - full / 2 - fast / 3- faster / 4- skip):\n""" % ('/'*50))
        if speed != 4:
            raw_input("""\n%s\nLearning Ready. \nThe computer will now play 117 games against itself to learn
the best strategy in the game environment you have just designed. \nPress Enter to begin\n%s\n""" \
% ('/'*50, '/'*50))
            if speed == 3: print "Learning... Please wait."
            game.learn(player2,speed)
        else:
            print "\nSkipping learning, playing on default game intelligence.\n"

    #randomly determine the game order
    print "\nThe turn order has been randomly determined: "
    if random.randint(0,1) == 0:
        game.active = 0 #sets active player
        print player1.name.capitalize() + ' (X) will go first, ' +\
              player2.name + ' (O) will go second.'
    else:
        game.active = 1
        print player2.name.capitalize() + ' (O) will go first, ' +\
              player1.name + ' (X) will go second.'
        
    raw_input("\n%s\nGame Ready. Press Enter to begin.\n%s\n" %('/'*50, '/'*50))
            
    #plays the game
    while True:
        game.play_game(player1, player2)
        rematch = input("""Press 1 to rematch or 2 to leave this game: """)
        if rematch != 1:
            print "\nGame Ended"
            break
        print "\n\n\n\n"
    

while True:
    main()
    again = input("Press 1 to restart the program, or 2 to exit: ")
    if again != 1:
        break
    print "\n\n\n\n"


