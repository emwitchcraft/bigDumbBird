from icecream import ic
import bigDumbBird
import sys
if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input('gimme file:')

board = bigDumbBird.Board(file)
scr = bigDumbBird.ScriptWriter(file, 'boardToQ1')

outline = board.getOutline()
bc = ic(board.getBoundingCoordinates())

shiftX = ic(-1 * bc['minX'])
shiftY = ic(-1 * bc['minY'])

scr += 'group all'
scr += f'move (>0 0) ({shiftX} {shiftY})'

scr.save()
