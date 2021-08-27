import bigDumbBird as bdb
import configparser
import os
import os.path as osp
import bigDumbBirdPathParser
from pathlib import Path
from icecream import ic

class PartsSourceList:
    #path should be the path to the .brd file you're generating the sourcing list from
    def __init__(self, path):
        parsedPath = bigDumbBirdPathParser.BigDumbBirdPathParser(path)
        partsSourceListPath = Path.joinpath(Path(bdb.getEaglesNest()), 
                                           *['partsSourcing', parsedPath.getPath('company', 'version')])
        if not Path.exists(partsSourceListPath):
            Path.mkdir(partsSourceListPath, parents=True)
        self.savePath = Path.joinpath(partsSourceListPath, parsedPath.nest["name"]).with_suffix('.bdbpsl')
        self.parts = configparser.ConfigParser(interpolation=None)
        self.parts[f'{parsedPath.nest["name"]} Parts Sourcing'] = {}
        self.mainList = configparser.ConfigParser(interpolation=None)
        self.mainList.read(Path.joinpath(Path(bdb.getEaglesNest()), 'partsSourcing', 'main.bdbpsl'))
        
    def add(self, value, package):
        id = f'{value}|{package}'
        if id in self.mainList.sections():
            self.parts[id] = self.mainList[id]
        else:
            self.parts[id] = {'price': 0, 'housePrice': 0, 'link': '', 'over5mm': 'false', 'notes': ''}
        
    def save(self):
        with open(self.savePath, 'w') as file:
            self.parts.write(file)

class PartsSourceListReader:
    def __init__(self, file):
        while Path(file).exists() is False:
            file = input(f'cant find source list\n {file}\n gimme one: ')
        self.parts = configparser.RawConfigParser()
        self.parts.read(file)
        
    def partInList(self, value, package):
        return f'{value}|{package}' in self.parts.sections()
        
    def getPrice(self, value, package):
        return self.parts.getfloat(f'{value}|{package}', 'price') \
                if self.partInList(value, package) \
                else 0
    
    def getHousePrice(self, value, package):
        return self.parts.getfloat(f'{value}|{package}', 'housePrice') if self.partInList(value, package) else 0
    
    def isOver5mm(self, value, package):
        return self.parts.getboolean(f'{value}|{package}', 'over5mm', fallback=False)
    
    def numPackagesOver5mm(self):
        return sum(1 for part in self.parts.sections() if self.parts.getboolean(part, 'over5mm', fallback=False))
    
    def numOfUniqueComponents(self):
        return len(self.parts.sections()) - 1
    
def addToMainSourceList(mainPslFile, newPslFile):
    main = configparser.ConfigParser(interpolation=None)
    main.read(mainPslFile)
    new = configparser.ConfigParser(interpolation=None)
    new.read(newPslFile)
    for i,section in enumerate(new.sections()):
        if i > 0 and 'client supplied' not in (new[section]['link'], new[section]['notes']):
            main[f'{section}'] = new[section]
    with open(mainPslFile, 'w') as file:
        main.write(file)

def makeSourceListFromUnsourcedParts(pslFile):
    psl = configparser.ConfigParser()
    psl.read(pslFile)
    missingList = configparser.ConfigParser()
    pslPath = bigDumbBirdPathParser.BigDumbBirdPathParser(pslFile)
    missingList[f'{pslPath.nest["name"]} Unsourced Parts'] = {}
    for i,part in enumerate(psl.sections()):
        if i > 0 and 'look for substitute' in psl[part]['link']:
            missingList[part] = psl[part]
    with open(Path.joinpath(Path(bdb.getEaglesNest()), *[pslPath.getPath('talon', 'version'), f'{pslPath.nest["name"]}Unsourced.bdbpsl']), 'w') as file:
        missingList.write(file)

def cleanSourceList():
    pslFile = input('psl file: ')
    psl = configparser.ConfigParser()
    psl.read(pslFile)
    for i,section in enumerate(psl.sections()):
        if i > 0:
            psl.remove_option(section, 'houseprice')
    with open(pslFile, 'w') as file:
        psl.write(file)
    
if __name__ == '__main__':
    mainListPath = osp.join(bdb.getEaglesNest(), 'partsSourcing', 'main.bdbpsl')
    newListPath = input('gimme psl to merge: ')
    addToMainSourceList(mainListPath, newListPath)
    
    #pslFile = input('original psl:')
    #makeSourceListFromUnsourcedParts(pslFile)
    #cleanSourceList()