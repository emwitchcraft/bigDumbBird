import bigDumbBird
import sys
import os
import sys
import partsSourceList as psl

saveDirectory = os.path.join(bigDumbBird.getEaglesNest(), 'boms')
if os.path.exists(saveDirectory) != True:
    os.makedirs(saveDirectory)
#bom = {value: {package: {ids:[], quantity}}}
def buildBom(parts, path):
    bom = {}
    missingValues = False
    generate = input('generate parts sourcing list? (y/n)')
    sourcingList = psl.PartsSourceList(path) if generate == 'y' else None
    
    for part in parts:
        value = part.get('value')
        package = part.get('package')
        partId = part.get('name')
        if value == '':
            print (f'{part.get("name")} has no value!')
            missingValues = True
            continue
        elif value not in bom:
            bom[value] = {package: {'ids': [partId], 'quantity': numUnits}}
        elif package not in bom[value]:
            bom[value][package] = {'ids': [partId], 'quantity': numUnits}
            
        else:
            bom[value][package]['quantity'] += numUnits
            bom[value][package]['ids'].append (partId)
            continue
        if sourcingList is not None:
            sourcingList.add(value, package)
    sourcingList.save()
    if missingValues:
        input ()
    return bom

def getFormatSpacing(bom):
    candidates = []
    for value in bom.keys():
        candidates.append(len((value)))
        for package in bom[value]:
            candidates.append(len(package))
    return int(max(candidates) / 4) + 2

def getFormattedString(string, spacing):
    tab = (spacing - (int(len(string) / 4))) * '\t'
    return f'{string}{tab}'
    
def formatBom(bom):
    s = getFormatSpacing(bom)
    add = lambda string: getFormattedString(string, s)
    output = [f'BOM for {numUnits} units\n']
    output += f'{add("Value")}{add("Package")}{add("Quantity")}{"IDs"}\n'
    output += f'{add("-----")}{add("-------")}{add("--------")}{add ("----")}\n'
    for value in bom.keys():
        for package in bom[value]:
            quantity = bom[value][package]['quantity']
            output += f'{add(f";{value};")}{add(f"{package};")}{add(f"{quantity};")}'
            for id in bom[value][package]['ids']:
                output += f'{id},'
            output.reverse ()
            output.remove (',')
            output.reverse ()
            output += '\n'
    return output

file = sys.argv[1] if len (sys.argv) > 1 else input ('gimme file:')
board = bigDumbBird.Board (file)
name = os.path.basename (file)
name = os.path.splitext(name)[0]
savePath = f'{saveDirectory}/{name}'

numUnits = int(input('how many units?'))
smdOnly = input ('smd only? (y/n)')
if smdOnly == 'y':
    parts = board.getAllSMDPartsInUse (returnAsElements=True)
    savePath = f'{savePath}SmdBOM.txt'
elif smdOnly == 'n':
    parts = board.getElements ()
    savePath = f'{savePath}BOM.txt'
    
with open (savePath, 'w') as file:
    file.writelines (formatBom(buildBom(parts, board.path)))
os.system (savePath)
    
""" except Exception as e:
    print(e)
    input() """