import eagleParse as ep
import sys
import os

if len (sys.argv) > 1: 
    board = ep.parseBoard (sys.argv[1] )
else:
    board = ep.parseBoard (input ('gimme file:'))

def getInfoString (component):
    return f'id: {component.name}   lib: {component.library}    package: {component.package}    value: {component.value}\n'



with open ('brdInfo.txt', 'w') as file:
    for comp in board.components:
        if comp.isSmd:
            file.write (getInfoString (comp))

os.system ('brdInfo.txt')
