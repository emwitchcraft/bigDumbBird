import bigDumbBird
import sys
if len (sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input ('gimme file:')
    
board = bigDumbBird.Board(file)

print(board.getWidthXHeight())
input()