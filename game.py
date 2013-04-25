#Game Class
#Gomoku Type Games - Lingliang Zhang / Comp Sci Assignment 4

#import relevant classes
from player import Player
from ai import AI
import copy
import time

class Game(object):
    def __init__(self):
        self.mode, self.length, self.win_con, self.player1, self.player2 = self.startup()
        self.active = 0
        self.speed = 0
        self.learning = 0
    
    #function to determine the game settings
    def startup(self):
        #intro message
        print "/" * 50 + "\nWelcome to Gomoku!\n By Lingliang \
Zhang (Intro to Comp Sci Assignment 4)\n" + "/"*50 + "\n"
        correct = 0
        #determine mode
        while correct == 0:
            #try and except added to prevent breaking on non-numerical inputs
            try:
                mode = input('What mode would you like to play? \n(1 for Single \
player / 2 for Multiplayer):\n')
                if mode != 1 and mode != 2: #check to see if mode is valid
                    print "Invalid input, please try again"
                else: correct = 1
            except:
                print "Invalid input, please try again."

        #choose size of game board
        correct = 0
        while correct == 0:
            try:
                length = input('\nHow long do you want the edge of the game board to be? \n(3-10):\n')
                if length <= 2 or length >= 11: #check to see if mode is valid
                    print "Invalid input, please enter a size between 3 and 10."
                else: correct = 1
            except:
                print "Invalid input, please enter a valid size between 3 and 10."

        #choose win condition
        correct = 0
        while correct == 0:
            try:
                win_con = input('\nHow many in a row should you need to make in a row to win? \
\n(greater than 2, less than or equal to the game board length): \n')
                if win_con < 3 or win_con > length: #check to see if mode is valid
                    print "Invalid input, please enter a length greater than 2, \n\
and less than or equal to the game board length"
                else: correct = 1
            except:
                print "Invalid input, please enter a valid length greater than 2, \n\
and less than or equal to the game board length"
        
        #Give the players appropriate names
        if mode == 1:
            player1, player2 = Player('you', 'X'), AI('the Computer', 'O')
        else:
            player1, player2 = Player('Player 1', 'X'), Player('Player 2', 'O')



        #return variables
        return mode, length, win_con, player1, player2


    #function which executes turns    
    def play_game(self, player1, player2):
        self.board = [[x*self.length+(y+1) for y in range(self.length)] for x in range(self.length)]
        self.remaining = [i for i in range(1,self.length**2+1)]    
        self.position_dict = {}
        
        #build the position dictionary
        for i in range(1,self.length**2+1):
            self.position_dict[i] = ((i-1)/self.length,(i-1)%self.length)

        self.draw_board()
        #loop to execute turns    
        for i in range(self.length**2):
            #determine whose turn it is
            if self.active%2 == 0:
                if self.mode == 1:
                    print "It is your turn." + " (X)"
                else:
                    print "It is Player 1's turn. (X)"
                player1.turn(self)
            else:
                print "It is " + player2.name + "'s turn. " + "(O)"
                player2.turn(self)

            self.active += 1

            self.draw_board()
                
            #check for winners
            win_symbol = self.check_winners()
            if win_symbol != None:
                if win_symbol == 'X':
                    winner = player1.name + '(X)'                  
                else:
                    winner = player2.name + '(O)'
                if self.mode == 1 and winner == player2.name + '(O)':
                    print '\n' + '/'*40 + '\nSorry! You lost!\n' + '/'*40 + '\n'
                    break
                else:
                    print '\n' + '/'*40+ '\n Congratulations! ' + winner.capitalize() +\
                    ' Won!\n' + '/'*40 + '\n'
                    break

        #condition if the game is a tie
        if win_symbol == None:
            print '\n' + '/'*40 + '\n' + 'The game is a draw.\n' + '/'*40 + '\n'


    #function to check if someone has won the game
    def check_winners(self):
        #build the list through which to check
        checklist = []
        for i in range(1, self.length+1):
            for element in self.pos_in_row(i):
                checklist.append(self.count_row(element))
            for element in self.pos_in_col(i):
                checklist.append(self.count_row(element))
        for element in self.pos_in_dia(0):
            checklist.append(self.count_row(element))
        for element in self.pos_in_dia(1):
            checklist.append(self.count_row(element))
    
        for check in checklist:
            if check['O'] == self.win_con:
                return 'O'
            if check['X'] == self.win_con:
                return 'X'


    #tallies the number of each piece in a row
    def count_row(self, row):
        row_tally = {'O': 0, 'X': 0, 0: 0}
        for position in row:
            val = self.board[self.position_dict[position][0]][self.position_dict[position][1]]
            if type(val) == int:
                val = 0
            row_tally[val] += 1
        return row_tally

    #function which returns list of positions in a row
    def pos_in_row(self, row_number):
        result = []
        for i in range(self.length-self.win_con+1):
            result.append(range((row_number-1)*self.length+1+i,(row_number-1)*self.length+1+i+self.win_con))
        return result

    #function which returns list of positions in a column
    def pos_in_col(self, col_number):
        result = []
        for i in range(self.length-self.win_con+1):
            result.append(range(col_number+i*(self.length), self.length*(self.win_con+i)+1, self.length))
        return result

    #funciton which returns list of positions in a diagonal (0 for left to right or 1 for right to left)
    def pos_in_dia(self, dia_number):
        x_pos = set([])
        y_pos = set([])
        result = []
        if dia_number == 0:
            for row_number in range(1, self.length-self.win_con+2):
                x_pos = x_pos.union(set(range((row_number-1)*self.length+1,(row_number-1)*self.length+self.length+1)))
                y_pos = y_pos.union(set(range(row_number, self.length**2+1, self.length)))
            for start_pos in x_pos.intersection(y_pos):
                result.append(range(start_pos,start_pos+(self.win_con-1)*(self.length+1)+1,self.length+1))
        if dia_number == 1:
            for row_number in range(1, self.length-self.win_con+2):
                x_pos = x_pos.union(set(range((row_number-1)*self.length+1,(row_number-1)*self.length+self.length+1)))
            for row_number in range(self.length, self.win_con-1, -1):
                y_pos = y_pos.union(set(range(row_number, self.length**2+1, self.length)))
            for start_pos in x_pos.intersection(y_pos):
                result.append(range(start_pos, start_pos + (self.win_con-1)*(self.length-1) + 1,self.length-1))
        return result

    
    #function to draw the game board
    def draw_board(self):
        for row in range(1+self.length*2):
            if row%2 == 0:
                print '-',
                for i in range(self.length):
                    print '--',
                    print '-',
                print
            else:
                for column in range(1+self.length*2):
                    if column%2 ==0:
                        print '|',
                    else:
                        if self.board[row/2][column/2] == 100:
                            print "100|",
                            break
                        elif len(str(self.board[row/2][column/2])) == 1:
                            print str(self.board[row/2][column/2]) + " ",
                        else:
                            print self.board[row/2][column/2],
                print
        print

    #begins the learning routine
    def learn(self, player, speed):
        old_ai = AI('Old AI', 'X')
        new_ai = AI('New AI', 'O')
        self.speed = speed
        counter = 0
        self.learning = 1
        start_time = time.clock()
                
        for i in range(10,0,-1):


            counter += 1
            new_ai.co1 += i
            self.mock_round(old_ai, new_ai, counter)
            if new_ai.co1 - i > 0:
                counter += 1
                new_ai.co1 -= i
                self.mock_round(old_ai, new_ai, counter)

            counter += 1
            new_ai.co2 += i
            self.mock_round(old_ai, new_ai, counter)
            if new_ai.co2 - i > 0:
                counter += 1
                new_ai.co2 -= i
                self.mock_round(old_ai, new_ai, counter)

            counter += 1
            new_ai.co3 += i
            self.mock_round(old_ai, new_ai, counter)
            if new_ai.co3 - i > 0:
                counter += 1
                new_ai.co3 -= i
                self.mock_round(old_ai, new_ai, counter)

            counter += 1
            new_ai.co3 += i
            self.mock_round(old_ai, new_ai, counter)
            if new_ai.co3 - i > 0:
                counter += 1
                new_ai.co3 -= i
                self.mock_round(old_ai, new_ai, counter)

            counter += 1
            new_ai.co4 += i
            self.mock_round(old_ai, new_ai, counter)
            if new_ai.co4 - i > 0:
                counter += 1
                new_ai.co4 -= i
                self.mock_round(old_ai, new_ai, counter)

            counter += 1
            new_ai.co5 += i
            self.mock_round(old_ai, new_ai, counter)
            if new_ai.co5 - i > 0:
                counter += 1
                new_ai.co5 -= i
                self.mock_round(old_ai, new_ai, counter)
            
        player.switch(old_ai)
        self.learning = 0
        print """\n%s\n%s\n%s\nFinished learning! %d games in %d seconds.
Final intelligence scores:\n (co1: %d co2: %d, co3: %d, co4: %d, co5: %d)\n%s\n%s\n%s\n""" % ('/'*40,'/'*40,'/'*40, counter,\
                                                                 time.clock() - start_time,\
                                                                 player.co1, player.co2, player.co3, player.co4, player.co5,\
                                                                         '/'*40,'/'*40,'/'*40)
                                                                 
    #controller of a mock game
    def mock_round(self, old_ai, new_ai, counter):
        if self.speed != 3:
            print new_ai.co1, new_ai.co2, new_ai.co3, new_ai.co4, new_ai.co5, 'NEW AI Intelligence'
            print old_ai.co1, old_ai.co2, old_ai.co3, old_ai.co4, old_ai.co5, 'OLD AI Intelligence'
        if self.play_mock_game(old_ai, new_ai, 1, counter) == 'O':
            old_ai.switch(new_ai)

        if self.speed != 3:
            print "\n%s\nEnd of game: %d. Current intelligence scores: \n (co1: %d co2: %d, co3: %d, co4: %d, co5: %d).\n%s\n"\
                  % ('/'*40, counter, old_ai.co1, old_ai.co2, old_ai.co3, old_ai.co4, old_ai.co5, '/'*40)
            time.sleep(0.3)
            
        new_ai.switch(old_ai)
        
        
        
    #the mock counterpart of play_game(), plays a mock game
    def play_mock_game(self, player1, player2, active, counter):
        self.board = [[x*self.length+(y+1) for y in range(self.length)] for x in range(self.length)]
        self.remaining = [i for i in range(1,self.length**2+1)]    
        self.position_dict = {}
        
        #build the position dictionary
        for i in range(1,self.length**2+1):
            self.position_dict[i] = ((i-1)/self.length,(i-1)%self.length)
        for i in range(self.length**2):
            #determine whose turn it is
            if active%2 == 0:
                if self.speed == 1:
                    print "It old AI's turn " + " (X)"
                    self.draw_board()
                    time.sleep(0.3)
                player1.turn(self)
            else:
                if self.speed == 1:
                    print "It is new AI's turn. " + "(O)"
                    self.draw_board()
                    time.sleep(0.3)
                player2.turn(self)

            active += 1
            
        

            #if self.speed == 1: self.draw_board()
                
            #check for winners
            win_symbol = self.check_winners()
            if win_symbol != None:
                if win_symbol == 'X':
                    winner = player1.name + '(X)'
                else:
                    winner = player2.name + '(O)'
                if self.speed != 3: print "\n%s\n%s Won!\n%s\n" % ('/'*40, winner, '/'*40)
                if self.speed == 2: self.draw_board()
                return win_symbol
        

        #condition if the game is a tie
        if win_symbol == None:
            if self.speed != 3: print '\n' + '/'*40 + '\n' + 'The game is a draw.\n' + '/'*40 + '\n'
        if self.speed == 2: self.draw_board()
        return win_symbol
        
    
