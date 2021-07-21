from icecream import ic
import bigDumbBird
import sys
if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input('gimme file:')

board = bigDumbBird.Board(file)
scr = bigDumbBird.ScriptWriter(file)

outline = board.getOutline()
bc = ic(board.getBoundingCoordinates())

shiftX = ic(-1 * bc['x0'])
shiftY = ic(-1 * bc['y0'])

scr += 'group all'
scr += f'move (>0 0) ({shiftX} {shiftY})'

scr.save()
