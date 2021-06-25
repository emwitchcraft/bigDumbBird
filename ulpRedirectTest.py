import bigDumbBird
from icecream import ic
import sys
import os.path as op

if len (sys.argv) > 1:
    file = ic (sys.argv[1])
else:
    file = input ('gimme file:')


#s = r'C:\Users\machew\Documents\EAGLE\projects\dummy\dummy2.brd'
c = bigDumbBird.ScriptWriter (file, 'ulpRedirectTest')
b = bigDumbBird.Board (file)
parts = b.getElements ()
for part in parts:
    part.set ('y', ic (str(float (part.get ('y')) + 10))) 
    c += f'move {part.get ("name")} ({part.get ("x")} {float (part.get ("y")) + 10})' 
c.save ()
#b.save ()
#sys.exit (c)