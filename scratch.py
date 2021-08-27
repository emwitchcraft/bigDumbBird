import configparser
import sys
from icecream import ic
import bigDumbBird

file = 'C:/users/machew/documents/eagle/projects/adventure/pedals/dreamReaper/smdV1_1/DreamReaperSMEDv1_2Drill.brd'

""" find all wires on given layer
    find extreme points and calc center"""
def findCenter(wires):
    xs = [float(x.get('x1')) for x in wires]
    xs.extend(float(x.get('x2')) for x in wires)
    ys = [float(wire.get('y2')) for wire in wires]
    ys.extend(float(y.get('y2')) for y in wires)
    midpoint = lambda p1,p2: p1 + ((p2 - p1) / 2)
    
    x = round(midpoint(min(xs), max(xs)), 2)
    y = round(midpoint(min(ys), max(ys)), 2)
    
    return x,y

board = bigDumbBird.Board(file)
parts = {'bias': '200',
            'vol': '201',
            'filter': '202',
            'sense': '203',
            'force': '204',
            'gain': '205',
            'cutoff': '206',
            'reap': '207',
            'range': '208',
            'dream': '209',
            'bypass': '210',
            'byp': '211',
            'fbk': '212'}

for part,layer in parts.items():
    wires = filter(lambda w: w.get('layer') == layer, board.plain.findall('wire'))
    x,y = findCenter(list(wires))
    print(f'move {part} ({x} {y})')
    

""" wires = board.plain.findall('wire')
for wire in wires:
    if wire.get('layer') == '200':
        print(wire.get('layer')) """

#I fxI1 fxO1 fxI2 fxO2 O
#I fxI2 fxO2 fxI1 fxO1 O