import eagleParse as ep
import smdInfo as smd
import sys
from icecream import ic

class FileWriter:
    def __init__ (self, path):
        self.name = path[path.rfind ('\\') + 1:path.rfind ('.')] + '.txt'
        self.createFile ()
    
    def createFile (self):
        with open (self.name, 'w') as file:
            file.write (f'{self.name} pnp pricing:\n')

    def add (self, string):
        with open (self.name, 'a') as file:
            file.write (f'{string}\n')

try:
    if len (sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input ('gimme file')
    board = ep.parseBoard (path)
    deets = FileWriter (path)    
        
except Exception as e:
    print (e)

#set up + pcb costs + screen + cost of parts 
#+ cost num unique parts + paste costs + per join cost
totalCost = 0
numPanels = float (input ('how many panels?'))
deets.add (ic.format (numPanels))

boardsPerPanel = float (input ('how many boards per panel?'))
deets.add (ic.format (boardsPerPanel))
totalBoards = boardsPerPanel * numPanels
deets.add (ic.format (totalBoards))

pcbFabCost = float (input ('how much for the boards?'))
deets.add (ic.format (pcbFabCost))

setUpNeeded = int (input ('setup needed?'))
deets.add (ic.format (setUpNeeded))
#cost for each component
componentCostPerPanel = 0
numComponentsPerPanel = 0
for comp in board.components:
    if comp.isSmd:
        if comp.library in ['Resistors', 'Capacitors'] and comp.package not in ['6.3X5.8SMD', '4X4.5SMD']:
            componentCostPerPanel += smd.prices[comp.library]
            numComponentsPerPanel += 1
        elif comp.package in smd.prices.keys ():
            componentCostPerPanel += smd.prices[comp.package]
            numComponentsPerPanel += 1
        elif comp.value in smd.prices.keys ():
            componentCostPerPanel += smd.prices[comp.value]
            numComponentsPerPanel += 1
        else:
            print (f'no price for id: {comp.id} value: {comp.value} package: {comp.package} from {comp.library}')
ic (componentCostPerPanel)
deets.add (ic.format (componentCostPerPanel))
ic (numComponentsPerPanel)
deets.add (ic.format (numComponentsPerPanel))

uniqueParts = []
for comp in board.components:
    if comp.isSmd:
        if comp.value == '':
            print (f'component has no value! id: {comp.id}')
        elif comp.value not in uniqueParts:
            uniqueParts.append (comp.value)
#ic (uniqueParts)
numUniqueParts = len (uniqueParts)
uniqueComponentCost = ic (smd.pricePerUniqueComponent * numUniqueParts)
deets.add (ic.format (numUniqueParts))
deets.add (ic.format (uniqueComponentCost))
ic (uniqueComponentCost)

solderJointCost = ic (smd.pricePerJoint * board.totalPads)
ic (solderJointCost)
deets.add (ic.format (board.totalPads))
deets.add (ic.format ('solderJointCost=pricePerJoint*totalPads'))
deets.add (ic.format (solderJointCost))

pasteCost = ic (smd.pasteDensitygmm3 * board.padArea * smd.stencilThickness * smd.pastePricePerGram)
ic (pasteCost)
deets.add (ic.format (board.padArea))
deets.add (ic.format ('pasteCost=pasteDensity(g/mm^3)*padArea*stencilThickness*pastePricePerGram'))
deets.add (ic.format (pasteCost))

firstTimeCost = ic ((smd.setUp + smd.stencilPrice) * setUpNeeded)
ic (firstTimeCost)
deets.add (ic.format ('firstTimeCost=(setUp + stencilPrice)*setUpNeeded'))
deets.add (ic.format (firstTimeCost))

s = f'perPanelCost=componentCostPerPanel+solderJointCost+pasteCost+(smd.laborPricePerBoard*boardsPerPanel)+smd.laborPricePerPanel'
deets.add (s)
perPanelCost = ic (componentCostPerPanel + solderJointCost + pasteCost + (smd.laborPricePerBoard * boardsPerPanel) + smd.laborPricePerPanel)
deets.add (ic.format (perPanelCost))
ic (perPanelCost)

s = 'totalPanelCost=(perPanelCost*numPanels)+uniqueComponentCost'
deets.add (s)
totalPanelCost = ic ((perPanelCost * numPanels) + uniqueComponentCost)
ic (totalPanelCost)
deets.add (ic.format (totalPanelCost))

totalCost = ic (firstTimeCost + pcbFabCost + totalPanelCost)
totalCost = round (totalCost, 2)
deets.add (ic.format ('totalCost=firstTimeCost+pcbFabCost+totalPanelCost'))
deets.add (ic.format (totalCost))
ic (totalCost)

deets.add ('effective prices are based on total cost of the order')
deets.add ('i.e. the same exact order will have lower price per unit')
deets.add ('if there\'s no setup or screen needed')

effectivePricePerPanel = totalCost / numPanels
ic (effectivePricePerPanel)
effectivePricePerPanel = round (effectivePricePerPanel, 2)
deets.add (ic.format (effectivePricePerPanel))

effectivePricePerBoard = effectivePricePerPanel / boardsPerPanel
effectivePricePerBoard = round (effectivePricePerBoard, 2)
ic (effectivePricePerBoard)
deets.add (ic.format (effectivePricePerBoard))

input ()