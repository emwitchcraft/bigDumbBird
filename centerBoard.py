import bigDumbBird
import sys
if len (sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input ('gimme file:')

board = bigDumbBird.Board(file)
scr = bigDumbBird.ScriptWriter(file, 'centerBoard')

outline = board.getOutline()
bc = board.getBoundingCoordinates()

deltaX = bc['maxX'] - bc['minX']
deltaY = bc['maxY'] - bc['minY']

shiftX = -1 * (deltaX / 2)
shiftY = -1 * (deltaY / 2)

scr += 'group all;'
scr += f'move (>0 0) ({shiftX} {shiftY});'

scr.save()