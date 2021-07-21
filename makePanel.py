import bigDumbBird
import sys
from icecream import ic
from shrinkPolygons import shrink

if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input('gimme file:')

#TODO hide layers when appropriate so the .scr runs faster

#get board info
board = bigDumbBird.Board(file)
scr = bigDumbBird.ScriptWriter(file)

#get board metrics
bounds = board.getBoundingCoordinates()
width,height = board.getWidthXHeight()

scr += 'grid mm finest'
#duplicate names to _tnames and _bnames
scr += 'layer 125 _tnames'
scr += 'layer 126 _bnames'
scr += 'display none tnames'
scr.groupAll()
scr += f'cut ({bounds["x0"]} {bounds["y0"]})'
scr += f'paste ({bounds["x0"]} {bounds["y0"]})'
scr += 'change layer _tnames (>0 0)'
scr += 'display none bnames'
scr.groupAll()
scr += f'cut ({bounds["x0"]} {bounds["y0"]})'
scr += f'paste ({bounds["x0"]} {bounds["y0"]})'
scr += 'change layer _bnames (>0 0)'
scr.displayAll()


#shrink polygon pour planes to 0.5mm from board edges
scr = shrink(board, scr)
#paste table hole spacing
gridX = 15
gridY = 13
#deets for mouseBite parts
mouseBiteSpacing = 2
mouseBiteHandleOffset = 0.25
maxDistanceBetweenBites = 70
halfBiteWidth = 2.75
outline = board.getOutline()
minX = None
maxX = None

#determine sides of pcb
for line in outline:
    x0 = float(line.get('x1'))
    xf = float(line.get('x2'))
    if x0 == xf:
        y = [float(line.get('y1')), float(line.get('y2'))]
        if minX == None or maxX == None:
            minX = x0
            maxX = x0
        elif x0 < minX:
            minX = x0
            leftY0 = min(y)
            leftYf = max(y)
        elif x0 > maxX:
            maxX = x0
            rightY0 = min(y)
            rightYf = max(y)

#place side bites
def addBites(x0, y0, yf, r):
    global scr
    addMouseBite = 'add mousebites_5arcs'
    if r == 90:
        xp = x0 - mouseBiteHandleOffset
    elif r == -90:
        xp = x0 + mouseBiteHandleOffset
    scr += f'{addMouseBite} r{r} ({xp} {y0 + halfBiteWidth})'
    scr += f'{addMouseBite} r{r} ({xp} {yf - halfBiteWidth})'
    delY = yf - y0
    if delY > maxDistanceBetweenBites:
        scr += f'{addMouseBite} r{r} ({xp} {y0 + (0.5 * delY)})'

addBites(minX, leftY0, leftYf, 90)
addBites(maxX, rightY0, rightYf, -90)

#TODO error check if resulting panel size is within max size (304.8mmX304.8mm for me)
#get panel matrix size from user and error check that it's a nonzero number
columns = ''
rows = ''
while columns == '':
    columns = int(input('how many columns?'))
    if columns == 0:
        columns = ''
while rows == '':
    rows = int(input('how many rows?'))
    if rows == 0:
        rows = ''

#calculate x-axis spacing for pcb to fit evenly between two tabs 
#with at least 4mm on either side of the baord for the tabs and mousebites
#results in a minimum tab width of 4mm and minimum 8mm b/t pcbs
#tabSpacingX should end up being a multiple of gridX
tabSpacingX = (int(width / gridX) + 1) * gridX
cushionX = (tabSpacingX - width) / 2
if cushionX < 4:
    tabSpacingX = (int(width / gridX) + 2) * gridX
    cushionX = (tabSpacingX - width) / 2

scr.displayAll()
#unlock everything
scr += 'lock -*'
#moves pcb to quadrant 1 and shifts to the right according to cushionX
scr += 'group all'
shiftX = (-1 * bounds['x0']) + cushionX
shiftY = (-1 * bounds['y0'])
scr += f'move (>0 0) ({shiftX} {shiftY})'
#copies pcb relative to the lower left corner
scr += f'cut ({cushionX} 0)'

#pastes the pcb copies
firstBoard = True
for r in range (rows):
    for c in range (columns):
        if firstBoard == False:
            x = (c * tabSpacingX) + cushionX
            y = (height * r) + ((r != 0) * mouseBiteSpacing)
            scr += f'paste ({x} {y})'
        else:
            firstBoard = False

#draws the panel tabs on dimension layer
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

#TODO check if 'toolingholes' library is in use and skip if it isn't
#adds tooling holes to the four corners tabs
totalHeight = ((height * rows) + ((rows - 1) * mouseBiteSpacing))
topPostPoint = int(totalHeight / gridY) * gridY
if (totalHeight - topPostPoint) < 3:
    topPostPoint -= gridY
rightMostPostPoint = tabSpacingX * columns
scr += f'add toolinghole4.2mm (0 {gridY})'
scr += f'add toolinghole4.2mm (0 {topPostPoint})'
scr += f'add toolinghole4.2mm ({rightMostPostPoint} {gridY})'
scr += f'add toolinghole4.2mm ({rightMostPostPoint} {topPostPoint})'


""" for bite in mouseBitesToDelete:
    scr += f'delete {bite}' """
#TODO skip next two commands if library isn't in use
scr += 'add tablepostperimeter (0 0)'
scr += 'add footbyfoot (0 0)'

#align panel to quadrant 1
scr += 'group all'
scr += f'move (>0 0) ({cushionX - mouseBiteSpacing} 0)'
scr.ratsNest()
scr += 'write'
scr += 'run cleanUpPanel'
scr.save()