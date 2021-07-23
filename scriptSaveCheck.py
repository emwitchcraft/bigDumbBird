import sys

if len(sys.argv) > 1:
    pyFile = sys.argv[1]
else:
    pyFile = input('gimme file:')

with open(pyFile, 'r') as file:
    f = file.read()
if 'ScriptWriter' in f:
    if '.save()' not in f:
        scrIndex = f.find('ScriptWriter(')
        nameStart = f.rfind('\n', 0, scrIndex) + 1
        name = f[nameStart:f.find('=', nameStart)]
        name = name.strip()
        with open(pyFile, 'a') as file:
            file.write(f'\n{name}.save()')