ulpDir = '/users/machew/documents/eagle/ulps/'
from icecream import ic
import sys
import os
bigDumbBirdDir = os.path.dirname(__file__).replace('\\', '/')

if len (sys.argv) > 1:
    pyFile = sys.argv[1]
else:
    pyFile = input ('gimme file:')

pyFile = pyFile.replace('\\', '/')
scriptName = pyFile[pyFile.rfind ('/') + 1:pyFile.rfind ('.')]
fullPath = f'{ulpDir}{scriptName}.ulp'
with open(pyFile, 'r') as file:
    pyFileContents = file.read()

ulp = 'string name;\n'
ulp += 'if (board) board (b)\n'
ulp += '{\n'
ulp += '    name = b.name;\n'
ulp += '}\n'
ulp += 'else if (schematic) schematic (s)\n'
ulp += '{\n'
ulp += '    name = s.name;\n'
ulp += '}\n'
if 'ScriptWriter' in pyFileContents:
    ulp += f'system ("py {bigDumbBirdDir}/scriptSaveCheck.py {pyFile}");\n'
ulp += f'system ("py {pyFile} " + name);\n'

if 'ScriptWriter' in pyFileContents:
    command = f'"script \'" + filesetext (name, "Scripts/{scriptName}.scr") + "\';";'
    ulp += f'string cmd = {command}\n'
    ulp += 'exit (cmd);'
else:
    ulp += 'exit (0);'

if os.path.exists(ulpDir) != True:
    os.makedirs(ulpDir)

with open (fullPath, 'w') as file:
    file.writelines (ulp)