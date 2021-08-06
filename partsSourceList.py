import bigDumbBird as bdb
import configparser
import os
import os.path as osp
from icecream import ic

class PartsSourceList:
    #don't need eagleFile argument if you're only going to use the read function
    def __init__(self, eagleFile=''):
        name = osp.splitext(osp.basename(eagleFile))[0]
        company = osp.split(osp.split(eagleFile)[0])[1]
        self.savePath = osp.join(bdb.getEaglesNest(), 'partsSourcing', company)
        if os.path.exists(self.savePath) != True:
            os.makedirs(self.savePath)
        self.savePath = osp.join(self.savePath, f'{name}.bdbpsl')
        self.parts = configparser.ConfigParser()
        self.parts[f'{name} Parts Sourcing'] = {}
        
    def add(self, value, package):
        self.parts[f'{value}|{package}'] = {'price': 0, 'link': '', 'over5mm': 'false', 'notes': ''}
        
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
    
    def isOver5mm(self, value, package):
        return self.parts.getboolean(f'{value}|{package}', 'over5mm', fallback=False)
    
    def numComponentsOver5mm(self):
        return sum(1 for part in self.parts.sections() if self.parts.getboolean(part, 'over5mm', fallback=False))
    
    def numOfUniqueComponents(self):
        return len(self.parts.sections()) - 1
    
    
