import bigDumbBird
import sys

dumbBirdFile = sys.argv[1] if len(sys.argv) > 1 else input('gimme file:')
scr = bigDumbBird.ScriptWriter(dumbBirdFile)
scr += 'display none 25 26 27 28'
scr.groupAll()
scr += 'change align center (>0 0)'
scr.displayAll()
scr.save()