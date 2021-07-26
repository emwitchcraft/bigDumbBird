import sys

pyFile = sys.argv[1] if len(sys.argv) > 1 else input('gimme file:')
with open(pyFile, 'r') as file:
    f = file.read()
if 'ScriptWriter' in f:
    scrIndex = f.find('ScriptWriter(')
    nameStart = f.rfind('\n', 0, scrIndex) + 1
    name = f[nameStart:f.find('=', nameStart)]
    name = name.strip()
    if f'{name}.save()' not in f:
        with open(pyFile, 'a') as file:
            file.write(f'\n{name}.save()')