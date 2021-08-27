import bigDumbBird
import sys

dumbBirdFile = sys.argv[1] if len(sys.argv) > 1 else input('gimme file:')

board = bigDumbBird.Board(dumbBirdFile, disableBackup=False)
scr = bigDumbBird.ScriptWriter(dumbBirdFile)

signals = board.getSignals()

def distance(x0, y0, xf, yf):
    delX = xf - x0
    delY = y0 - yf
    return ((delX ** 2) + (delY ** 2)) ** 0.5

def getCoords(wire):
    f = lambda w,i: float(w.get(i))
    return f(wire, 'x1'), f(wire, 'y1'), f(wire, 'x2'), f(wire, 'y2')

def getMid (x0, y0, xf, yf):
    return x0 + ((xf - x0) * 0.5), y0 + ((yf - y0) * 0.5)

onlyAirWires = lambda wire: wire.get('layer') == '19'
skipSignalsWithPlanePour = lambda signal: signal.find('polygon') is None

airWires = filter(onlyAirWires, [wire for signal in filter(skipSignalsWithPlanePour, signals) for wire in signal.findall('wire')])

maxDistance = float(input('max distance: '))
for airWire in airWires:
    x0, y0, xf, yf = getCoords(airWire)
    if distance(x0, y0, xf, yf) < maxDistance:
        mid = getMid(x0, y0, xf, yf)
        scr += f'route ({x0} {y0}) ({xf} {yf})'
scr.save()