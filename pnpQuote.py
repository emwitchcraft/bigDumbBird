import bigDumbBird
import partsSourceList as psl
import pnpDetails as pd
import sys
import os
from icecream import ic

eagleFile = sys.argv[1] if len(sys.argv) > 1 else input('gimme file:')
eagleName = os.path.splitext(os.path.basename(eagleFile))[0].replace('Panel', '')
company = os.path.split(os.path.split(eagleFile)[0])[1]
saveName = f'{eagleName}.quote'
savePath = os.path.join(bigDumbBird.getEaglesNest(), 'pnpQuotes', company, saveName)
if os.path.exists(savePath) != True:
    os.makedirs(savePath)

output = f'{eagleName} pnp assembly quote\n'
output += f'{"-" * (len(output) - 1)}\n'

board = bigDumbBird.Board(eagleFile)

partPricesPath = os.path.join(bigDumbBird.getEaglesNest(), 'partsSourcing', company, f'{eagleName}.bdbpsl')
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

if input('first run? (y/n)') == 'y':
    cost = pd.panelizing + pd.filePrep + pd.gerbering
    if quote['pcbFabCosts'] != 0:
        cost += pd.ordering + pd.stencilPrice
    add('firstRunSetup', cost)

add('pastingSetUp', pd.tableSetup)
add('uniqueComponents', sourceList.numOfUniqueComponents())
add('uniqueComponentCost', pd.pricePerUniqueComponent * sourceList.numOfUniqueComponents())

componentCostsPerPanel = sum(sourceList.getPrice(part.get('value'), part.get('package')) 
                                for part in board.getAllSMDPartsInUse(returnAsElements=True))
componentCostsPerPanel += sum(pd.pricePerComponentOver5mm for part in board.getAllSMDPartsInUse(returnAsElements=True)
                                if sourceList.isOver5mm(part.get('value'), part.get('package')))
add('componentCosts', componentCostsPerPanel * quote['numPanels'])

pasteCost = board.getTotalSMDArea() * pd.pasteDensitygmm3 * pd.stencilThickness * pd.pastePricePerGram
add('paste', quote['numPanels'] * pasteCost) 

solderCost = board.getTotalSMDPads() * pd.pricePerJoint
add('soldering', quote['numPanels'] * solderCost)




quote['perBoard'] = totalCost / quote['numBoards']
quote['perBoardNoComp'] = (totalCost - (componentCostsPerPanel * quote['numPanels'])) / quote['numBoards']
quote['totalNoComp'] = totalCost - (componentCostsPerPanel * quote['numPanels'])
quote['total'] = totalCost
for key in quote:
    ic(f'{key}: {quote[key]}')

    


