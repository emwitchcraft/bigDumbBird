import sys
sys.path.append ('/1vsCode/python/myTime')
import EST as est
from icecream import ic
import os

bomFiles = []
quantityPerBom = []
while 1:
    fileName = input ('gimme file or type "done"')
    if fileName == 'done':
        break
    else:
        numUnits = ic(int(input ('how many units?')))
        with open (fileName, 'r') as file:
            lines = list(filter(lambda line: line[0] == ';', file.readlines()))
        bomFiles.append({'numUnits': numUnits, 'lines': lines})

partDict = {}
for bom in bomFiles:
    for line in bom['lines']:
        line = line.strip('\n').strip(' ').replace('\t', '').split(';')
        if line[1] not in partDict.keys ():
            partDict[line[1]] = {'package': line[2], 'quantity': int (line[3]) * bom['numUnits']}
        else:
            partDict[line[1]]['quantity'] += int (line[3]) * bom['numUnits']

def assembleBom (bom, numUnits=1):
    longestStringLength = 0
    for value in bom.keys ():
        if len (value) > longestStringLength:
            longestStringLength = len (value)
        if len (bom[value]['package']) > longestStringLength:
            longestStringLength = len (bom[value]['package'])
    t = int (longestStringLength / 4) + 2       
    tab = lambda s: (t - (int (len (s) / 4))) * '\t'
    add = lambda a: f'{a}{tab(a)}'
    
    output = [f'{add ("Value")}{add ("Package")}{add ("Quantity")}\n']
    output += f'{add ("-----")}{add ("-------")}{add ("--------")}\n'
    for value,info in bom.items ():
        output += f'{add (f";{value};")}{add (info["package"] + ";")}{add (str (info["quantity"] * numUnits) + ";")}'
        output += '\n'
    return output

bom = assembleBom (partDict)
savePath = f'/1vsCode/python/bigDumbBird/totalUpBOMsOutput/{est.getStamp(type="date")}.txt'
with open (savePath, 'w') as file:
    file.writelines (bom)

os.system (ic (savePath))