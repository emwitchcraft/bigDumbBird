import bigDumbBird
import sys
from icecream import ic
from centerBoard import getShiftXYToCenterBoard as getShift
if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input('gimme file:')

board = bigDumbBird.Board(file)
scr = bigDumbBird.ScriptWriter(file, 'copyAndPlaceForPanel')
bounds = board.getBoundingCoordinates()
width,height = board.getWidthXHeight()
gridX = 15
gridY = 13
mouseBiteSpacing = 2

columns = int(input('how many columns?'))
rows = int(input('how many rows?'))

tabSpacingX = (int(width / gridX) + 1) * gridX
#tabSpacingY = (int(height / gridY) + 1) * gridY
cushionX = (tabSpacingX - width) / 2
if cushionX < 4:
    tabSpacingX = (int(width / gridX) + 2) * gridX
    cushionX = (tabSpacingX - width) / 2


scr += 'lock -*'
scr += 'group all'
shiftX = (-1 * bounds['x0']) + cushionX
shiftY = (-1 * bounds['y0'])
#shifts = getShift(bounds)
scr += f'move (>0 0) ({shiftX} {shiftY})'
scr += 'copy'

firstBoard = True
for r in range (rows):
    for c in range (columns):
        if firstBoard == False:
            x = (c + 0.5) * tabSpacingX
            y = (height / 2) + ((r * height) + (mouseBiteSpacing * (r != 0)))
            scr += f'paste ({x} {y})'
        else:
            firstBoard = False

for c in range (columns + 1):
    gap = cushionX - mouseBiteSpacing
    center = c * tabSpacingX
    xL = center - gap
    xR = center + gap
    scr.drawRect(xL,
                xR,
                0,
                (height * rows) + ((rows - 1) * mouseBiteSpacing),
                20)


scr += 'add tablepostperimeter (0 0)'
scr += 'add footbyfoot (0 0)'
scr.save()