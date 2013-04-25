#Gomoku
#By Lingliang Zhang
#Intro to Computer Science - Assignment #4
#Creates a gomoku game board, on which both singleplayer and multiplayer game modes
#can be played. Incorporates a proprietary AI (Plays perfectly in 3x3)
#The user defines the rules of the game, the size of the board and how many pieces in
#a row are required to win. The AI will play 117 games against itself to determine the
#best strategy in this game world.

gomoku.py is the driver file

Features:
- User defines the game board length and how many pieces in a row are required to win
- The AI will play 117 games against itself to determine the best strategy in the user defined game world
- The AI has 3 learning speeds - 1. Move by Move, 2. Show only end-states, 3. Hide all learning