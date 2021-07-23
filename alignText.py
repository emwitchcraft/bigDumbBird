import bigDumbBird
import sys


if len(sys.argv) > 1:
    dumbBirdFile = sys.argv[1]
else:
    dumbBirdFile = input('gimme file:')

scr = bigDumbBird.ScriptWriter(dumbBirdFile)
scr += 'display none 25 26 27 28'
scr.groupAll()
scr += 'change align center (>0 0)'
scr.displayAll()
scr.save()