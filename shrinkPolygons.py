import bigDumbBird
import sys
from icecream import ic

def shrink(board, scr):
    bounds = board.getBoundingCoordinates()
    signals = board.getSignals()
    for signal in signals:
        polygon = signal.find('polygon')
        if polygon != None:
            for vertex in polygon.findall('vertex'):
                x = float(vertex.get('x'))
                y = float(vertex.get('y'))
                x0 = bounds['x0']
                xf = bounds['xf']
                y0 = bounds['y0']
                yf = bounds['yf']
                
                newX = None
                newY = None
                if x < x0:
                    newX = x0 - 0.5
                elif xf < x:
                    newX = xf + 0.5
                if y < y0:
                    newY = y0 - 0.5
                elif yf < y:
                    newY = yf + 0.5    
                    #scr.drawRectGroup(bounds=bounds)
                baseCmd = f'move ({x} {y})'
                if newX != None and newY == None:
                    scr += f'{baseCmd} ({newX} {y})'
                elif newX == None and newY != None:
                    scr += f'{baseCmd} ({x} {newY})'
                elif newX != None and newY != None:
                    scr += f'{baseCmd} ({newX} {newY})'
    return scr

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = input('gimme file:')

    board = bigDumbBird.Board(file)
    scr = bigDumbBird.ScriptWriter(file)


    scr = shrink(board, scr)
    scr.save()