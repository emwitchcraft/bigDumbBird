import bigDumbBird as bdb
import configparser
import os
import os.path as osp

class PartsSourceList:
    def __init__(self, eagleFile):
        name = osp.splitext(osp.basename(eagleFile))[0]
        self.savePath = osp.join(bdb.getEaglesNest(), 'partsSourcing')
        if os.path.exists(self.savePath) != True:
            os.makedirs(self.savePath)
        self.savePath = osp.join(self.savePath, f'{name}PartsSourcing.bdbpsl')
        self.parts = configparser.ConfigParser()
        self.parts[f'{name} Parts Sourcing'] = {}
        
    def add(self, part, package):
        self.parts[f'{part}|{package}'] = {'price': '', 'link': '', 'notes': ''}
        
    def save(self):
        with open(self.savePath, 'w') as file:
            self.parts.write(file)


    
