import bigDumbBird
import sys

def shrink(board, scr):
    bounds = board.getBoundingCoordinates()
    signals = board.getSignals()
    x0 = bounds['x0']
    xf = bounds['xf']
    y0 = bounds['y0']
    yf = bounds['yf']
    for signal in signals:
        polygon = signal.find('polygon')
        if polygon != None:
            for vertex in polygon.findall('vertex'):
                x = float(vertex.get('x'))
                y = float(vertex.get('y'))
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
                baseCmd = f'move ({x} {y})'
                if newX is not None and newY is None:
                    scr += f'{baseCmd} ({newX} {y})'
                elif newX is None and newY is not None:
                    scr += f'{baseCmd} ({x} {newY})'
                elif newX is not None:
                    scr += f'{baseCmd} ({newX} {newY})'
    return scr

if __name__ == '__main__':
    file = sys.argv[1] if len(sys.argv) > 1 else input('gimme file:')
    board = bigDumbBird.Board(file)
    scr = bigDumbBird.ScriptWriter(file)


    scr = shrink(board, scr)
    scr.save()