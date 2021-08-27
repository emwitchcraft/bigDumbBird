import bigDumbBird
import partsSourceList
import sys
import bigDumbBirdPathParser

eagleFile = sys.argv[1] if len(sys.argv) > 1 else input('gimme file:')

bigDumbPath = bigDumbBirdPathParser.BigDumbBirdPathParser(eagleFile)
pslPath = bigDumbPath.getPathWithReplacement('talon', 'ext', 'talon', 'partsSourcing')
pslReader = partsSourceList.PartsSourceListReader(pslPath)

board = bigDumbBird.Board(eagleFile)
totalClientCost = 0
totalHouseCost = 0
for component in board.getAllSMDPartsInUse(returnAsElements=True):
    value = component.get('value')
    package = component.get('package')
    if pslReader.partInList(value, package):
        totalClientCost += pslReader.getPrice(value, package)
        totalHouseCost += pslReader.getHousePrice(value, package)
    else:
        print(f'{value}|{package} not in source list')
        input()

quantity = int(input('how many boards?'))
totalClientCost *= quantity
totalHouseCost *= quantity

spread = totalClientCost - totalHouseCost

output = f'total client cost: {totalClientCost}\n'
output += f'total house cost: {totalHouseCost}\n'
output += f'spread: {spread}'

print(output)