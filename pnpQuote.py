import bigDumbBird
import partsSourceList as psl
import pnpDetails as pd
import sys
import os
from icecream import ic

eagleFile = sys.argv[1] if len(sys.argv) > 1 else input('gimme file:')
eagleName = os.path.splitext(os.path.basename(eagleFile))[0]
pslName = eagleName[:eagleName.find('Panel')]
project = os.path.split(os.path.split(eagleFile)[0])[1]
company = os.path.split(os.path.split(os.path.split(eagleFile)[0])[0])[1]
saveName = f'{eagleName}Quote.txt'
savePath = os.path.join(bigDumbBird.getEaglesNest(), 'pnpQuotes', company, project)
if os.path.exists(savePath) != True:
    os.makedirs(savePath)
savePath = os.path.join(savePath, saveName)

board = bigDumbBird.Board(eagleFile)

partPricesPath = os.path.join(bigDumbBird.getEaglesNest(), 'partsSourcing', company, project, f'{pslName}.bdbpsl')
if not os.path.exists(partPricesPath):
    partPricesPath = input('cant find part sourcing file, pls gimme:')
sourceList = psl.PartsSourceListReader(partPricesPath)

totalCost = 0

quote = {'numPanels': float(input('how many panels?')),
            'boardsPerPanel': float(input('how many boards per panel?'))}
quote['numBoards'] = quote['numPanels'] * quote['boardsPerPanel']

def add(item, price):
    global quote, totalCost
    totalCost += price
    quote[item] = price

add('labor', (quote['numPanels'] * pd.pricePerPanel) + (quote['numBoards'] * pd.pricePerBoard))
add('pcbFabCosts', float(input('how much for the boards?')))
quote['pcbFabCostsPerBoard'] = quote['pcbFabCosts'] / quote['numBoards']

if input('first run? (y/n)') == 'y':
    add('*panelizing', pd.panelizing)
    add('*pnpFilePrep', pd.filePrep)
    add('*gerbering', pd.gerbering) 
    add('*stencil', pd.stencilPrice)
    firstRun = True
else:
    firstRun = False
    
if quote['pcbFabCosts'] != 0:
    add('ordering', pd.ordering) 

add('pastingSetUp', pd.tableSetup)
#add('uniqueComponents', sourceList.numOfUniqueComponents())
add('uniqueComponentCost', pd.pricePerUniqueComponent * sourceList.numOfUniqueComponents())

componentCostsPerPanel = 0
houseCompCostPerPanel = 0
componentsOver5mmPerPanel = 0
for part in board.getAllSMDPartsInUse(returnAsElements=True):
    value = part.get('value')
    package = part.get('package')
    componentCostsPerPanel += sourceList.getPrice(value, package)
    if sourceList.isOver5mm(value, package):
        componentsOver5mmPerPanel += pd.pricePerComponentOver5mm
    houseCompCostPerPanel += sourceList.getHousePrice(value, package)

add('componentCosts', componentCostsPerPanel * quote['numPanels'])
quote['componentCostsPerBoard'] = quote['componentCosts'] / quote['numBoards']
add('componentsOver5mm', componentsOver5mmPerPanel * quote['numPanels'])

houseCompCost = houseCompCostPerPanel * quote['numPanels']
compSpread = quote['componentCosts'] - houseCompCost

pasteCost = board.getTotalSMDArea() * pd.pasteDensitygmm3 * pd.stencilThickness * pd.pastePricePerGram
add('paste', quote['numPanels'] * pasteCost) 

solderCost = board.getTotalSMDPads() * pd.pricePerJoint
add('soldering', quote['numPanels'] * solderCost)

panelArea = board.getArea()
packagingMaterialCost = panelArea * 2 * pd.bubbleWrapPermm2
add('packaging', packagingMaterialCost * quote['numPanels'])
if input('any misc? (y/n)') == 'y':
    add(input('what for?'), float(input('how much?')))
quote['total'] = round(totalCost, 2)
quote['totalNoPcbs'] = round(totalCost - quote['pcbFabCosts'] - quote['ordering'], 2)
quote['totalNoComponents'] = round(totalCost - quote['componentCosts'], 2)
quote['totalNoComponentsNoPcbs'] = round(quote['totalNoPcbs'] - quote['componentCosts'], 2)
quote['perBoard'] = round(totalCost / quote['numBoards'], 2)
quote['perBoardNoPcbs'] = round(quote['totalNoPcbs'] / quote['numBoards'], 2)
quote['perBoardNoComponents'] = round(quote['totalNoComponents'] / quote['numBoards'], 2)
quote['perBoardNoComponentsNoPcbs'] = round(quote['totalNoComponentsNoPcbs'] / quote['numBoards'], 2)
for key in quote:
    print(f'{key}: {quote[key]}')

profitish = quote['totalNoPcbs'] - houseCompCost - quote['paste'] 
if 'stencil' in quote:
    profitish -= quote['stencil']
print(f'houseCompCost: {houseCompCost}')
print(f'compSpread: {compSpread}')
print(f'profitish: {profitish}')
print(f'profitishPerBoard: {profitish / quote["numBoards"]}')

longestString = max(len(item) for item in quote)

output = f'{eagleName} pnp assembly quote\n'
output += f'{"-" * (len(output) - 1)}\n'
formattedString = lambda thing,cost,prefix,suffix: f'{thing}{"-" * ((longestString - len(thing)) + 4)}{prefix}{cost}{suffix}\n'
for thing,cost in quote.items():
    prefix = '$' if thing not in ['numPanels', 'boardsPerPanel', 'numBoards'] else ''
    suffix = ' + paypal fees + shipping' if thing == 'total' else ''
    output += formattedString(thing, cost, prefix, suffix)
    if thing == 'packaging': output += '\n'
output += '\n'
minToStart = quote['componentCosts'] + quote['pcbFabCosts']
if firstRun: minToStart += quote['*stencil']
output += formattedString('minimumDueToStart', round(minToStart, 2), '$', '')
output += '(components + pcbFab + stencil)' if firstRun else '(components + pcbFab)'
if firstRun: output += '\n\n*only incurred on the first run of a board'
with open(savePath, 'w') as file:
    file.write(output)
os.system(savePath)