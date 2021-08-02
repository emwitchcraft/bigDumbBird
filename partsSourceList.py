import configparser
import os

class PartsSourceList:
    def __init__(self, eagleFile):
        c = configparser.ConfigParser()
        c.read('C:/1vsCode/python/bigDumbBird/bigDumbBird.config')
        eaglePath = c.get('paths', 'eagle')
        splitPath = os.path.splitext(eagleFile)
        name = os.path.basename(splitPath[0])
        self.savePath = f'{eaglePath}/partsSourcing/{name}PartsSourcing.bdbpsl'
        if os.path.exists(os.path.dirname(self.savePath)) != True:
            os.makedirs(os.path.dirname(self.savePath))
        self.parts = configparser.ConfigParser()
        self.parts[f'{name} Parts Sourcing'] = {}
    
    def add(self, part, package):
        self.parts[f'{part}|{package}'] = {'price': '', 'link': '', 'notes': ''}
        
    def save(self):
        with open(self.savePath, 'w') as file:
            self.parts.write(file)


    
