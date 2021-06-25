import eagleParse as ep
import sys
import os
import smdInfo as smd

if len (sys.argv) > 1:
    board = ep.parseBoard (sys.argv[1])
else:
    board = ep.parseBoard (input ('gimme file:'))

with open ('packageList.txt', 'w') as file:
    for p in board.packages:
        if p.find ('smd') != None:
            if p.get ('name') not in smd.packages:
                file.write (f'add to package list: ')
            file.write (p.get ('name') + '\n')

os.system ('packageList.txt')
