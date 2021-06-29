#change to where you want to save the BOM
saveDirectory = '/users/machew/documents/eagle/boms'
from icecream import ic
import bigDumbBird
import sys
sys.path.append ('/1vsCode/python/myOS')
import os
import sys
if len (sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input ('gimme file:')
smdOnly = input ('smd only? (y/n)')
board = bigDumbBird.Board (file)
name = os.path.basename (file)
name = name[:name.rfind('.')]
savePath = f'{saveDirectory}/{name}'
bom = {}
if smdOnly == 'y':
    parts = board.getAllSMDPartsInUse (returnAsElements=True)
    savePath = f'{savePath}SmdBOM.txt'
elif smdOnly == 'n':
    parts = board.getElements ()
    savePath = f'{savePath}BOM.txt'
    
#total  
missingValues = False
for part in parts:
    value = part.get('value').casefold()
    if value == '':
        print (f'{part.get("name")} has no value!')
        missingValues = True
    elif value not in bom.keys ():
        info = {'ids': [part.get ('name')], 'package': part.get ('package'), 'quantity': 1}
        bom[value] = info
    elif value in bom.keys ():
        bom[value]['quantity'] += 1
        bom[value]['ids'].append (part.get ('name'))

if missingValues:
    input ()
#tab = lambda t: t * '\t'

def assembleBom ():
    longestStringLength = 0
    for value in bom.keys ():
        if len (value) > longestStringLength:
            longestStringLength = len (value)
        if len (bom[value]['package']) > longestStringLength:
            longestStringLength = len (bom[value]['package'])
    t = int (longestStringLength / 4) + 2       
    tab = lambda s: (t - (int (len (s) / 4))) * '\t'
    add = lambda a: f'{a}{tab(a)}'
    
    output = [f'{add ("Value")}{add ("Package")}{add ("Quantity")}{"IDs"}\n']
    output += f'{add ("-----")}{add ("-------")}{add ("--------")}{add ("----")}\n'
    for value,info in bom.items ():
        output += f'{add (f";{value};")}{add (info["package"] + ";")}{add (str (info["quantity"]) + ";")}'
        for id in info['ids']:
            output += f'{id},'
        output.reverse ()
        output.remove (',')
        output.reverse ()
        output += '\n'
    return output

bomLines = assembleBom ()
with open (savePath, 'w') as file:
    file.writelines (bomLines)
os.system (savePath)