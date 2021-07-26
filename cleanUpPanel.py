import bigDumbBird
import sys

file = sys.argv[1] if len(sys.argv) > 1 else input('gimme file:')
board = bigDumbBird.Board(file)
scr = bigDumbBird.ScriptWriter(file)

for element in board.getElements():
    if float(element.get('y')) <= -0.25 and element.get('library') == 'mouseBites':
        scr += f'delete {element.get("name")}'
scr.save()