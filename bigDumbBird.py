import xml.etree.ElementTree as et
import sys
sys.path.append ('/1vsCode/python/myOS')
import myOS

class Schematic:
    def __init__ (self, file):
        self.path = file
        self.tree = et.parse (file)
        self.root = self.tree.getroot ()
        
        self.drawing = self.root.find('drawing')
        
        self.settings = self.drawing.find ('settings')
        self.grid = self.drawing.find ('grid')
        self.layers = self.drawing.find ('layers')
        self.schematic = self.drawing.find ('schematic')
        
        self.libraries = self.schematic.find ('libraries')
        self.classes = self.schematic.find ('classes')
        self.parts = self.schematic.find ('parts')
        self.sheets = self.schematic.find ('sheets')
        
    def getParts (self):
        return self.parts.findall ('part')
    
    def getLayers (self):
        return self.layers.findall ('layer')
    
    def getSheets (self):
        return self.sheets.findall ('sheet')
    
    def save (self):
        self.tree.write (self.path, encoding='UTF-8')
    
class Board:
    def __init__ (self, file):
        self.path = file
        self.tree = et.parse (file)
        self.root = self.tree.getroot ()
        
        self.drawing = self.root.find ('drawing')
        
        self.settings = self.drawing.find ('settings')
        self.grid = self.drawing.find ('grid')
        self.layers = self.drawing.find ('layers')
        self.board = self.drawing.find ('board')
        
        self.plain = self.board.find ('plain')
        self.libraries = self.board.find ('libraries')
        self.classes = self.board.find ('classes')
        self.designRules = self.board.find ('designrules')
        self.yourAreAChumpIfYouUseTheAutoRouter = self.board.find ('autorouter')
        self.elements = self.board.find ('elements')
        self.signals = self.board.find ('signals')
        
    def getElements (self):
        return self.elements.findall ('element')
        
    def getLayers (self):
        return self.layers.findall ('layer')
    
    def getLibrariesInUse (self):
        return self.libraries.findall ('library')
    
    def getSignals (self):
        return self.signals.findall ('signal')
    
    def getPackagesInUse (self):
        packages = [packages for library in self.getLibrariesInUse () for packages in library.find ('packages')]
        return packages
    
    def getBoundingPerimeter (self):
        wires = filter (lambda wire: wire.get ('layer') == '20', self.plain.findall ('wire'))
        Xs = []
        Ys = []
        for wire in wires:
            Xs.extend ([float (wire.get ('x1')), float (wire.get ('x2'))])
            Ys.extend ([float (wire.get ('y1')), float (wire.get ('y2'))])
        minX = min (Xs)
        maxX = max (Xs)
        minY = min (Ys)
        maxY = max (Ys)
        return (maxX - minX, maxY - minY)
                
    def save (self):
        self.tree.write (self.path, encoding='UTF-8', xml_declaration=True)

class ScriptWriter:
    def __init__ (self, path, scrName):
        self.commands = []
        self.path = f'{path[:path.rfind (".")]}/{scrName}.scr'
        myOS.createIfNonExistent (self.path[:self.path.rfind ('/')])
        
    def __iadd__ (self, command):
        command = str (command)
        self.commands.append (f'{command};\n')
        return self
    
    def save (self):
        myOS.createIfNonExistent (self.path[:self.path.rfind ('/')])
        self.commands.append ('write;')
        with open (self.path, 'w') as file:
            file.writelines (self.commands)
    

