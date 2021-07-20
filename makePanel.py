import bigDumbBird
import sys
from icecream import ic
from shrinkPolygons import shrink

if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input('gimme file:')

board = bigDumbBird.Board(file)
scr = bigDumbBird.ScriptWriter(file, 'makePanel')
scr = shrink(board, scr)
bounds = board.getBoundingCoordinates()
width,height = board.getWidthXHeight()
gridX = 15
gridY = 13
mouseBiteSpacing = 2

mouseBitesToDelete = []
for element in board.getElements():
    if float(element.get('y')) < bounds['y0']:
        mouseBitesToDelete.append(element.get('name'))

columns = int(input('how many columns?'))
rows = int(input('how many rows?'))

tabSpacingX = (int(width / gridX) + 1) * gridX
cushionX = (tabSpacingX - width) / 2
if cushionX < 4:
    tabSpacingX = (int(width / gridX) + 2) * gridX
    cushionX = (tabSpacingX - width) / 2


scr += 'lock -*'
scr += 'group all'
shiftX = (-1 * bounds['x0']) + cushionX
shiftY = (-1 * bounds['y0'])
scr += f'move (>0 0) ({shiftX} {shiftY})'
scr += f'cut ({cushionX} 0)'

firstBoard = True
for r in range (rows):
    for c in range (columns):
        if firstBoard == False:
            x = (c * tabSpacingX) + cushionX
            y = (height * r) + ((r != 0) * mouseBiteSpacing)
            scr += f'paste ({x} {y})'
        else:
            firstBoard = False

for c in range (columns + 1):
    gap = cushionX - mouseBiteSpacing
    center = c * tabSpacingX
    xL = center - gap
    xR = center + gap
    scr.drawRect(20,
                x0=xL,
                xf=xR,
                y0=0,
                yf=(height * rows) + ((rows - 1) * mouseBiteSpacing))

totalHeight = ((height * rows) + ((rows - 1) * mouseBiteSpacing))
topPostPoint = int(totalHeight / gridY) * gridY
if (totalHeight - topPostPoint) < 3:
    topPostPoint -= gridY
rightMostPostPoint = tabSpacingX * columns
scr += f'add toolinghole4.2mm (0 {gridY})'
scr += f'add toolinghole4.2mm (0 {topPostPoint})'
scr += f'add toolinghole4.2mm ({rightMostPostPoint} {gridY})'
scr += f'add toolinghole4.2mm ({rightMostPostPoint} {topPostPoint})'


for bite in mouseBitesToDelete:
    scr += f'delete {bite}'
scr += 'add tablepostperimeter (0 0)'
scr += 'add footbyfoot (0 0)'
scr += 'group all'
scr += f'move (>0 0) ({cushionX - mouseBiteSpacing} 0)'
scr.ratsNest()
scr.save()