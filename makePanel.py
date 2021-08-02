import bigDumbBird
import sys
from shrinkPolygons import shrink

dumbBirdFile = sys.argv[1] if len(sys.argv) > 1 else input('gimme file:')
#get board info
board = bigDumbBird.Board(dumbBirdFile, disableBackup=False)
#board.saveBackup('MakePanelBackup')
scr = bigDumbBird.ScriptWriter(dumbBirdFile)

#center align all text if it isn't already
scr += 'display none 25 26 27 28'
scr.groupAll()
scr += 'change align center (>0 0)'
scr.displayAll()
scr += 'write'

#reload brd 
#(something about the internal paste buffer fucks up 
# keeping pads connected to their nets if you don't do a clean load)
scr += f'edit {dumbBirdFile}'

#get board metrics
bounds = board.getBoundingCoordinates()
width,height = board.getWidthXHeight()

#duplicate names to _tnames and _bnames
tnames = '25'
bnames = '26'
_tnames = '125'
_bnames = '126'
scr += f'layer {_tnames} _tnames'
scr += f'set color_layer {_tnames} 5'
scr += f'layer {_bnames} _bnames'
scr += f'set color_layer {_bnames} 13'
scr += f'display none'# {_tnames} {_bnames}'
for element in board.getElements():
    for attribute in element.findall('attribute'):
        if attribute.get('name') == 'NAME':
            name = element.get('name')
            x = attribute.get('x')
            y = attribute.get('y')
            size = attribute.get('size')
            ratio = attribute.get('ratio')
            rot = attribute.get('rot')
            if rot is None:
                rot = 'r0'
            align = attribute.get('align')
            if attribute.get('layer') in [tnames, 'tplace', '21']:
                layer = _tnames
            elif attribute.get('layer') in [bnames, 'bplace', '22']:
                layer = _bnames
            scr += f'change layer {layer}'
            scr += f'change size {size}'
            scr += f'change ratio {20}'
            if align is not None:
                scr += f'change align {align}'
            scr += f'text \'{name}\' {rot} ({x} {y})'


#shrink polygon pour planes to 0.5mm from board edges
scr.displayAll()
scr = shrink(board, scr)
scr += 'display none'
#paste table hole spacing
gridX = 15
gridY = 13
#deets for mouseBite parts
mouseBiteSpacing = 2
mouseBiteHandleOffset = 0.25
maxDistanceBetweenBites = 75
halfBiteWidth = 2.75
outline = board.getOutline()

#determine sides of pcb
#haven't tested it, but will probably break correct bite placement
# if the sides consist of more than one segment
minX = None
maxX = None
for line in outline:
    x0 = float(line.get('x1'))
    xf = float(line.get('x2'))
    y = [float(line.get('y1')), float(line.get('y2'))]
    if x0 == xf:
        if minX is None or maxX is None:
            minX = x0
            maxX = x0
            leftY0 = min(y)
            leftYf = max(y)
            rightY0 = leftY0
            rightYf = leftYf
        if x0 < minX:
            minX = x0
            leftY0 = min(y)
            leftYf = max(y)
        elif x0 > maxX:
            maxX = x0
            rightY0 = min(y)
            rightYf = max(y)

#place side bites
def addBites(x0, y0, yf, rot):
    global scr
    addMouseBite = 'add mousebites_5arcs'
    if rot == 90:
        xp = x0 - mouseBiteHandleOffset
    elif rot == -90:
        xp = x0 + mouseBiteHandleOffset
    y0 += halfBiteWidth
    yf -= halfBiteWidth
    line = lambda y: f'{addMouseBite} r{rot} ({xp} {y})'
    scr += line(y0)
    scr += line(yf)
    delY = yf - y0
    if delY > maxDistanceBetweenBites:
        scr += line(y0 + (0.5 * delY))

scr += 'display none 20'
addBites(minX, leftY0, leftYf, 90)
addBites(maxX, rightY0, rightYf, -90)
scr += 'display none'
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

#calculate panel dimensions
#error check if resulting panel size is within max size (304.8mmX304.8mm for me)
#if not, subtract a board from the panel until it's small enough
fitsInOven = False
maxDimension = 304
while not fitsInOven:
    #calculate x-axis spacing for pcb to fit evenly between two tabs 
    #with at least 4mm on either side of the board for the tabs and mousebites
    #results in a minimum tab width of 4mm and minimum 8mm b/t pcbs
    #tabSpacingX should end up being a multiple of gridX
    tabSpacingX = (int(width / gridX) + 1) * gridX
    cushionX = (tabSpacingX - width) / 2
    if cushionX < 4:
        tabSpacingX = (int(width / gridX) + 2) * gridX
        cushionX = (tabSpacingX - width) / 2
    totalWidth = (columns * tabSpacingX) + (2 * cushionX)
    if totalWidth > maxDimension:
        columns -= 1
    totalHeight = (height * rows) + ((rows - 1) * mouseBiteSpacing)
    if totalHeight > maxDimension:
        rows -= 1
    if totalWidth < maxDimension and totalHeight < maxDimension:
        fitsInOven = True

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
        if not firstBoard:
            x = (c * tabSpacingX) + cushionX
            y = (height * r) + (r * mouseBiteSpacing)
            scr += f'paste ({x} {y})'
        else:
            firstBoard = False

#draws the panel tabs on dimension layer
scr += 'display none 20'
for c in range (columns + 1):
    gap = cushionX - mouseBiteSpacing
    center = c * tabSpacingX
    xL = center - gap
    xR = center + gap
    scr.drawRect(20,
                x0=xL,
                xf=xR,
                y0=0,
                yf=totalHeight)

#TODO check if 'toolingholes' library is in use and skip if it isn't
#adds tooling holes to the four corners tabs
topPostPoint = int(totalHeight / gridY) * gridY
if (totalHeight - topPostPoint) < 3:
    topPostPoint -= gridY
rightMostPostPoint = tabSpacingX * columns
line = lambda x,y: f'add toolinghole4.2mm ({x} {y})'
scr += line(0, gridY)
scr += line(0, topPostPoint)
scr += line(rightMostPostPoint, gridY)
scr += line(rightMostPostPoint, topPostPoint)


""" for bite in mouseBitesToDelete:
    scr += f'delete {bite}' """
#TODO skip next two commands if library isn't in use
scr += 'add tablepostperimeter (0 0)'

#align panel to quadrant 1
scr.displayAll()
scr += 'group all'
scr += f'move (>0 0) ({cushionX - mouseBiteSpacing} 0)'
scr.ratsNest()
scr += 'add footbyfoot (0 0)'
scr += 'write'
scr += 'run cleanUpPanel'
scr.save()