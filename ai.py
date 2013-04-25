#AI Class
#Gomoku Type Games - Lingliang Zhang / Comp Sci Assignment 4

from player import Player
import copy
import random
import math

class AI(Player):
    def __init__(self, name, symbol):
        #Borrows parent co-efficients
        Player.__init__(self, name, symbol)
        #initilise intelligence co-efficients
        self.co1 = 24
        self.co2 = 16
        self.co3 = 7
        self.co4 = 10
        self.co5 = 10
        if self.symbol == 'X':
            self.opponent = 'O'
        else:
            self.opponent = 'X'

    def turn(self, game):
        #intilise variables
        self.position_type = {}
        self.position_points = {}
        self.points_tally = {}
        for i in range(1,game.length**2+1):
            self.position_type[i] = [0,0]
            self.position_points[i] = [0,0,0] #[attack,defend,neutral]
            self.points_tally[i] = 0
        #thinks about all possible moves, adding points for all squares

        self.count_points(game)
        #decides the best turn and makes it
        for position in range(1,game.length**2+1):
            #check special condition - attacking from corners is especially good if piece in 
            if game.length == 3:
                if set([2,4,6,8]).issubset(game.remaining) and position in [1,3,7,9]:
                    #defending on corners is especially bad if enemy controls other corners
                    if self.symbol not in [game.board[0][0], game.board[0][2], game.board[2][0], game.board[2][2]]\
                       and self.opponent in [game.board[0][0], game.board[0][2], game.board[2][0], game.board[2][2]]:
                        self.position_points[position][1] /= 8 
                    #defending corner forks on corners is especially bad


            #Compute all other points through the elementwise vector multiplication
            self.points_tally[position] += self.position_points[position][0]*((self.position_type[position][0]**2))\
                                            + self.position_points[position][1]*((self.position_type[position][1]**2))
        
        highest_val = 0
        highest_pos = 0

        for key in self.points_tally:
            if self.points_tally[key] > highest_val:
                highest_val = self.points_tally[key]
                highest_pos = key

        if highest_pos == 0:
            highest_pos = game.remaining[0]


        self.replace(game, game.position_dict[highest_pos])
        game.remaining.remove(highest_pos)
            

    def count_points(self, game):
        if self.symbol == 'O':
            index = 1
        else:
            index = 0
        #counts the points in each row, column and diagonal
        checklist = []
        
        for i in range(1, game.length+1):
            checklist.append(game.pos_in_row(i))
            checklist.append(game.pos_in_col(i))
        checklist.append(game.pos_in_dia(0))
        checklist.append(game.pos_in_dia(1))

        for major_row in checklist:
            for row in major_row:
                row_tally = game.count_row(row)
                if len(game.remaining) == game.length**2 and game.length == 3:
                    self.points_tally[1] += 1000000000
                    
                for position in row:
                    if position in game.remaining:
                        
                        #condition 0.1: Imminent victory
                        if row_tally[self.symbol] == game.win_con-1 and row_tally[self.opponent] == 0 and game.learning == 0:
                                self.points_tally[position] += 1000000000**2
                        elif row_tally[self.symbol] == game.win_con-2 and row_tally[self.opponent] == 0 and game.learning == 0:
                                self.points_tally[position] += 10000000**2

                        #condition 0.2: Imminent defeat
                        elif row_tally[self.opponent] == game.win_con-1 and row_tally[self.symbol] == 0 and game.learning == 0:
                                self.points_tally[position] += 100000000**2
                        elif row_tally[self.opponent] == game.win_con-2 and row_tally[self.symbol] == 0 and game.learning == 0:
                                self.points_tally[position] += 1000000**2


                        #condition 2: blank row
                        elif row_tally[self.symbol] + row_tally[self.opponent] == 0:
                            self.points_tally[position] += self.co1
                            

                        #condition 1: Attacking row
                        elif row_tally[self.opponent] == 0:
                            self.position_type[position][int(math.fabs(index-1))] += 1            
                            self.position_points[position][int(math.fabs(index-1))] += self.co2+row_tally[self.symbol]*self.co4
                    
                

                        #condition 3: Defending row
                        elif row_tally[self.symbol] == 0:
                            self.position_type[position][index] += 1
                            self.position_points[position][index] += self.co3+row_tally[self.opponent]*self.co5
                            
    def switch(self, other):
        self.co1 = copy.copy(other.co1)
        self.co2 = copy.copy(other.co2)
        self.co3 = copy.copy(other.co3)
        self.co4 = copy.copy(other.co4)
        self.co5 = copy.copy(other.co5)

