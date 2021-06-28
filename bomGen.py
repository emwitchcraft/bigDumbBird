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
numUnits = int (input ('how many units?'))
board = bigDumbBird.Board (file)

savePath = f'{file[:file.rfind (".")]}SmdBOM.txt'
bom = {}
if smdOnly == 'y':
    parts = board.getAllSMDPartsInUse (returnAsElements=True)
    savePath = f'{file[:file.rfind (".")]}SmdBOM.txt'
elif smdOnly == 'n':
    parts = board.getElements ()
    savePath = f'{file[:file.rind (".")]}BOM.txt'
for part in parts:
    if part.get ('value') not in bom.keys ():
        info = {'ids': [part.get ('name')], 'package': part.get ('package'), 'quantity': 1}
        bom[part.get ('value')] = info
    elif part.get ('value') in bom.keys ():
        bom[part.get ('value')]['quantity'] += 1
        bom[part.get('value')]['ids'].append (part.get ('name'))

#tab = lambda t: t * '\t'

def assembleBom (numUnits=1):
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
        if numUnits == 1:
            output += f'{add (value)}{add (info["package"])}{add (str (ic (info["quantity"])))}'
        elif numUnits > 1:
            output += f'{add (f";{value};")}{add (info["package"] + ";")}{add (str (info["quantity"] * numUnits) + ";")}'
        for id in info['ids']:
            output += f'{id},'
        output.reverse ()
        output.remove (',')
        output.reverse ()
        output += '\n'
    return output

bomLines = assembleBom ()
bomLines += '\n\n'
bomLines += f'for {numUnits} units:\n'
bomLines += assembleBom (numUnits=numUnits)
with open (savePath, 'w') as file:
    file.writelines (bomLines)
    
os.system (savePath)