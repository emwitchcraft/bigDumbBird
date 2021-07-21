import bigDumbBird
import sys

if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input('gimme file:')

board = bigDumbBird.Board(file)
scr = bigDumbBird.ScriptWriter(file)

for element in board.getElements():
    if float(element.get('y')) <= -0.25 and element.get('library') == 'mouseBites':
        scr += f'delete {element.get("name")}'
scr.save()