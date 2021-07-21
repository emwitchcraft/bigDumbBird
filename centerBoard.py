import bigDumbBird
import sys
if len (sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input ('gimme file:')

board = bigDumbBird.Board(file)
scr = bigDumbBird.ScriptWriter(file)

outline = board.getOutline()
bc = board.getBoundingCoordinates()

def getShiftXYToCenterBoard(bounds):
    deltaX = bounds['xf'] - bounds['x0']
    deltaY = bounds['yf'] - bounds['y0']

    centerX = bounds['x0'] + (deltaX / 2)
    centerY = bounds['y0'] + (deltaY / 2)
    shiftX = -1 * centerX
    shiftY = -1 * centerY
    return shiftX,shiftY

shifts = getShiftXYToCenterBoard(bc)
#scr += 'write;'
scr += 'group all;'
scr += f'move (>0 0) ({shifts[0]} {shifts[1]});'

scr.save()