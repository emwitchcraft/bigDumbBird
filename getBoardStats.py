import bigDumbBird 
import sys
from icecream import ic

if len (sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input ('gimme file:')

board = bigDumbBird.Board (file)

x,y = ic (board.getBoundingPerimeter ())
boundedArea = ic (x * y)