import bigDumbBird
import sys
file = sys.argv[1] if len(sys.argv) > 1 else input('gimme file:')
board = bigDumbBird.Board(file)
scr = bigDumbBird.ScriptWriter(file)

outline = board.getOutline()
bc = board.getBoundingCoordinates()

shiftX = -1 * bc['x0']
shiftY = -1 * bc['y0']

scr += 'group all'
scr += f'move (>0 0) ({shiftX} {shiftY})'

scr.save()
