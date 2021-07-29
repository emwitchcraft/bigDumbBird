#change to where you want to save the BOM
saveDirectory = '/users/machew/documents/eagle/boms'
import bigDumbBird
import sys
import os
import sys

file = sys.argv[1] if len (sys.argv) > 1 else input ('gimme file:')

numUnits = int(input('how many units?'))
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
#bom = {value: {package: {ids:[], quantity}}}
missingValues = False
for part in parts:
    value = part.get('value').casefold()
    package = part.get('package')
    partId = part.get('name')
    if value == '':
        print (f'{part.get("name")} has no value!')
        missingValues = True
    elif value not in bom:
        bom[value] = {package: {'ids': [partId], 'quantity': numUnits}}
    elif package not in bom[value]:
        bom[value][package] = {'ids': [partId], 'quantity': numUnits}
    else:
        bom[value][package]['quantity'] += numUnits
        bom[value][package]['ids'].append (partId)

if missingValues:
    input ()

def getLongestStringLength(bom):
    candidates = []
    for value in bom.keys():
        candidates.append(len((value)))
        for package in bom[value]:
            candidates.append(len(package))
    return max(candidates)

longestStringLength = getLongestStringLength(bom)
t = int (longestStringLength / 4) + 2       
tab = lambda s: (t - (int (len (s) / 4))) * '\t'
add = lambda a: f'{a}{tab(a)}'

def getHeader():
    string = [f'BOM for {numUnits} units\n']
    string += f'{add ("Value")}{add ("Package")}{add ("Quantity")}{"IDs"}\n'
    string += f'{add ("-----")}{add ("-------")}{add ("--------")}{add ("----")}\n'
    return string
    
def assembleBom():
    output = getHeader()
    for value in bom.keys():
        for package in bom[value]:
            quantity = bom[value][package]['quantity']
            output += f'{add (f";{value};")}{add (f"{package};")}{add (f"{quantity};")}'
            for id in bom[value][package]['ids']:
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