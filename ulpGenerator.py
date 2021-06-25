ulpDir = '/users/machew/documents/eagle/ulps/'#use '/' or '\\'

from icecream import ic
import sys
sys.path.append ('/1vsCode/python/myOS')
import myOS

if len (sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input ('gimme file:')

file = file.replace('\\', '/')
scriptName = file[file.rfind ('/') + 1:file.rfind ('.')]
fullPath = f'{ulpDir}{scriptName}.ulp'

executionType = input ('execute as ulp or scr?')

ulp = 'string name;\n'
ulp += 'if (board) board (b)\n'
ulp += '{\n'
ulp += '    name = b.name;\n'
ulp += '}\n'
ulp += 'else if (schematic) schematic (s)\n'
ulp += '{\n'
ulp += '    name = s.name;\n'
ulp += '}\n'
ulp += f'system ("py {file} " + name);\n'
if executionType == 'ulp':
    command = '"edit " + name;'
elif executionType == 'scr':
    command = f'"script \'" + filesetext (name, "/{scriptName}.scr") + "\';";'
ulp += f'string cmd = {command}\n'
ulp += 'exit (cmd);'

myOS.createIfNonExistent (ulpDir)
with open (fullPath, 'w') as file:
    file.writelines (ulp)