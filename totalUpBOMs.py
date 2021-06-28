import sys
sys.path.append ('/1vsCode/python/myTime')
import EST as est
from icecream import ic
import os

bomFiles = []

while 1:
    inp = input ('gimme file or type "done"')
    if inp == 'done':
        break
    else:
        bomFiles.append (inp)
        
quantitiedLines = []
for bom in bomFiles:
    with open (bom, 'r') as file:
        lines = file.readlines ()
    for line in lines:
        if line[0] == ';':
            quantitiedLines.append (line[1:])
partDict = {}
for line in quantitiedLines:
    line = ic (line.strip ('\n').strip (' ').replace ('\t', '').split (';'))
    if line[0] not in partDict.keys ():
        partDict[line[0]] = {'package': line[1], 'quantity': int (line[2])}
    else:
        partDict[line[0]]['quantity'] += int (line[2])

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
        if numUnits == 1:
            output += f'{add (value)}{add (info["package"])}{add (str (ic (info["quantity"])))}'
        elif numUnits > 1:
            output += f'{add (f";{value};")}{add (info["package"] + ";")}{add (str (info["quantity"] * numUnits) + ";")}'
        output += '\n'
    return output

bom = assembleBom (partDict)
savePath = f'/1vsCode/python/bigDumbBird/totalUpBOMsOutput/{est.getStamp(type="date")}.txt'
with open (savePath, 'w') as file:
    file.writelines (bom)

os.system (ic (savePath))