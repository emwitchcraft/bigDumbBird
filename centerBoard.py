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

centerX = bc['minX'] + (deltaX / 2)
centerY = bc['minY'] + (deltaY / 2)
shiftX = -1 * centerX
shiftY = -1 * centerY

#scr += 'write;'
scr += 'group all;'
scr += f'move (>0 0) ({shiftX} {shiftY});'

scr.save()