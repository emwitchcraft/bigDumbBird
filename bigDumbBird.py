import xml.etree.ElementTree as et
import sys
sys.path.append ('/1vsCode/python/myOS')
import myOS
from icecream import ic

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
    
    def reloadBoard(self):
        self.__init__(self.path)
        
    def getElements(self):
        return self.elements.findall ('element')
        
    def getLayers(self):
        return self.layers.findall ('layer')
    
    def getLibrariesInUse(self):
        return self.libraries.findall ('library')
    
    def getSignals(self):
        return self.signals.findall ('signal')
    
    def getPackagesInUse(self):
        packages = [packages for library in self.getLibrariesInUse () for packages in library.find ('packages')]
        return packages
    
    #returns everything on layer20 (dimension)
    def getOutline(self):
        return filter(lambda wire: wire.get('layer') == '20', self.plain.findall('wire'))
    
    def getBoundingCoordinates(self):
        wires = self.getOutline()
        Xs = []
        Ys = []
        for wire in wires:
            Xs.extend ([float (wire.get ('x1')), float (wire.get ('x2'))])
            Ys.extend ([float (wire.get ('y1')), float (wire.get ('y2'))])
        bounds = {}
        bounds['x0'] = min (Xs)
        bounds['xf'] = max (Xs)
        bounds['y0'] = min (Ys)
        bounds['yf'] = max (Ys)
        return bounds
        
    def getWidthXHeight(self):
        bounds = self.getBoundingCoordinates()
        return (bounds['xf'] - bounds['x0'], bounds['yf'] - bounds['y0'])
    
    """ 'returnAsElements=False will return just the names as strings instead of the full etree elements """
    def getAllSMDPackagesInUse(self, returnAsElements=False):
        smdPackages = []
        for package in self.getPackagesInUse ():
            if package.find ('smd') != None:
                if returnAsElements:
                    smdPackages.append (package)
                else:
                    smdPackages.append (package.get ('name'))
        return smdPackages
    
    """ 'returnAsElements=False will return just the names as strings instead of the full etree elements """
    def getAllSMDPartsInUse(self, returnAsElements=False):
        smdPackages = self.getAllSMDPackagesInUse ()
        smdParts = []
        for element in self.getElements ():
            if element.get ('package') in smdPackages:
                if returnAsElements:
                    smdParts.append (element)
                else:
                    smdParts.append (element.get ('name'))
        return smdParts
    
    def getTotalSMDPads(self):
        parts = self.getAllSMDPartsInUse (returnAsElements=True)
        packages = self.getAllSMDPackagesInUse (returnAsElements=True)
        totalSMDPads = 0
        for part in parts:
            for package in packages:
                if part.get ('package') == package.get ('name'):
                    totalSMDPads += len (package.findall ('smd'))
                    break
        return totalSMDPads            
    
    def getTotalSMDArea(self):
        parts = self.getAllSMDPartsInUse (returnAsElements=True)
        packages = self.getAllSMDPackagesInUse (returnAsElements=True)
        f = lambda p: float (p.get ('dx')) * float (p.get ('dy'))
        areaPerPackage = {package.get ('name'): sum ([f (pad)]) for package in packages for pad in package.findall ('smd')}
        totalSMDArea = sum ([areaPerPackage[part.get ('package')] for part in parts])
        return totalSMDArea  
    
    def save(self):
        self.tree.write (self.path, encoding='UTF-8', xml_declaration=True)

class ScriptWriter:
    def __init__(self, path, pythonProgramName):
        self.commands = []
        self.path = f'{path[:path.rfind (".")]}Scripts/{pythonProgramName}.scr'
        myOS.createIfNonExistent (self.path[:self.path.rfind ('/')])
        
    def __iadd__(self, command):
        command = str (command)
        self.commands.append (f'{command};\n')
        return self
    
    def save(self):
        myOS.createIfNonExistent (self.path[:self.path.rfind ('/')])
        self.commands.append ('write;')
        with open (self.path, 'w') as file:
            file.writelines (self.commands)
    
    def drawRectGroup(self, x0=0, xf=0, y0=0, yf=0, bounds=None):
        if bounds != None:
            x0 = bounds['x0']
            xf = bounds['xf']
            y0 = bounds['y0']
            yf = bounds['yf']
        command = f'group ({x0} {y0}) ({x0} {yf}) ({xf} {yf}) ({xf} {y0}) ({x0} {y0})\n'
        self.commands += command
    
    def drawRect(self,layer, x0 = 0, xf = 0, y0 = 0, yf = 0, bounds=None):
        self.commands += f'layer {layer}\n'
        if bounds != None:
            x0 = bounds['x0']
            xf = bounds['xf']
            y0 = bounds['y0']
            yf = bounds['yf']
        self.commands += f'line 0 ({x0} {y0}) ({x0} {yf}) ({xf} {yf}) ({xf} {y0}) ({x0} {y0})\n'

    def ratsNest(self, ripUpPolygonsAfter=True):
        self.commands.append('ratsnest;\n')
        if ripUpPolygonsAfter:
            self.commands.append('ripup @;\n')
