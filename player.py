#Player Class
#Gomoku Type Games - Lingliang Zhang / Comp Sci Assignment 4

class Player():
    def __init__(self, name,symbol):
        self.name = name
        self.symbol = symbol

    #function that governs a turn
    def turn(self, game):
        correct = 0
        #ask where the player would like to place their piece
        while correct == 0:
            try:
                pos = input('Please type the position you would like to place your piece: ')
                if pos in game.remaining:
                    correct = 1
                else:
                    print "Error: invalid input, please try again!!!. \n"
            except:
                print "Error: invalid input, please try again, \n"

        game.remaining.remove(pos)
        self.replace(game, game.position_dict[pos])
        
    def replace(self, game, position):
        game.board[position[0]][position[1]] = self.symbol


    
    
