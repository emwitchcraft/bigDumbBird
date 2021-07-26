import bigDumbBird
import sys
file = sys.argv[1] if len (sys.argv) > 1 else input ('gimme file:')
board = bigDumbBird.Board(file)

print(board.getWidthXHeight())
input()