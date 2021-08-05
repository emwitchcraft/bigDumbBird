import bigDumbBird as bdb
import configparser
import os
import os.path as osp

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
        
    def add(self, part, package):
        self.parts[f'{part}|{package}'] = {'price': 0, 'link': '', 'over5mm': 'false', 'notes': ''}
        
    def save(self):
        with open(self.savePath, 'w') as file:
            self.parts.write(file)

class PartsSourceListReader:
    def __init__(self, file):
        self.parts = configparser.ConfigParser()
        self.parts.read(file)
        """ self.parts = {part: c.getfloat(part, 'price') 
                        for i, part in enumerate(c.sections()) 
                        if i > 0} """
    def getPrice(self, part, package):
        return self.parts.getfloat(f'{part}|{package}', 'price')
    
    def isOver5mm(self, part, package):
        return self.parts.getboolean(f'{part}|{package}', 'over5mm')
    
    def getNumberOfParts(self):
        return len(self.parts.sections()) - 1
    
    
