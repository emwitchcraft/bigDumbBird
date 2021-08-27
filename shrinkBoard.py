import bigDumbBird
import sys
#only good for rectangular boards
dumbBirdFile = sys.argv[1] if len(sys.argv) > 1 else input('gimme file:')

board = bigDumbBird.Board(dumbBirdFile)
scr = bigDumbBird.ScriptWriter(dumbBirdFile)

spacing = int(input('how much border space? (relative to center of most extreme components)'))

parts = board.getElements()
getCoord = lambda x: (float(part.get(x)) for part in parts)
minX = min(getCoord('x'))
maxX = max(getCoord('x'))
minY = min(getCoord('y'))
maxY = max(getCoord('y'))

bounds = board.getBoundingCoordinates()

scr += f'move ({bounds["x0"]} {bounds["yf"]}) ({minX - spacing} {maxY + spacing})'
scr += f'move ({bounds["xf"]} {bounds["yf"]}) ({maxX + spacing} {maxY + spacing})'
scr += f'move ({bounds["xf"]} {bounds["y0"]}) ({maxX + spacing} {minY - spacing})'
scr += f'move ({bounds["x0"]} {bounds["y0"]}) ({minX - spacing} {minY - spacing})'


scr.save()