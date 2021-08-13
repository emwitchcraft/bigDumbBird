import bigDumbBird as bdb
import configparser
import os
import os.path as osp

class PartsSourceList:
    #don't need eagleFile argument if you're only going to use the read function
    def __init__(self, eagleFile=''):
        path = osp.splitext(eagleFile)[0]
        name = osp.basename(path)
        version = osp.basename(osp.split(path)[0])
        project = osp.basename(osp.split(osp.split(path)[0])[0])
        if 'adventure' in path:
            category = osp.basename(osp.split(osp.split(osp.split(path)[0])[0])[0])
            self.savePath = osp.join(bdb.getEaglesNest(), 'partsSourcing', 'adventure', category, project, version)
        else:
            company = osp.basename(osp.split(osp.split(osp.split(path)[0])[0])[0])
            self.savePath = osp.join(bdb.getEaglesNest(), 'partsSourcing', company, project, version)
        if os.path.exists(self.savePath) != True:
            os.makedirs(self.savePath)
        self.savePath = osp.join(self.savePath, f'{name}.bdbpsl')
        self.parts = configparser.ConfigParser()
        self.parts[f'{name} Parts Sourcing'] = {}
        self.mainList = configparser.ConfigParser()
        self.mainList.read(osp.join(bdb.getEaglesNest(), 'partsSourcing', 'main.bdbpsl'))
        
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
        self.parts = configparser.ConfigParser()
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
    main = configparser.ConfigParser()
    main.read(mainPslFile)
    new = configparser.ConfigParser()
    new.read(newPslFile)
    for i,section in enumerate(new.sections()):
        if i > 0 and 'client supplied' not in [new[section]['link'], new[section[['notes']]]]:
            main[f'{section}'] = new[section]
    with open(mainPslFile, 'w') as file:
        main.write(file)
            
if __name__ == '__main__':
    mainListPath = osp.join(bdb.getEaglesNest(), 'partsSourcing', 'main.bdbpsl')
    newListPath = input('gimme psl to merge: ')
    addToMainSourceList(mainListPath, newListPath)