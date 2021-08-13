import pathlib

#./your/path/to/EAGLE/talon/company/category/design/version/name.ext
#ex: ./users/me/documents/EAGLE/projects/adventure/pedals/dreamReaper/v1_4/dreamReaperV1_4Panel2X2.brd
class BigDumbBirdPathParser:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        nestDex = self.path.parts.index('EAGLE')
        dex = lambda i: self.path.parts[nestDex + i]
        self.nest = {'talon': dex(1),
                    'company': dex(2),
                    'category': dex(3),
                    'design': dex(4),
                    'version': dex(5),
                    'name': self.path.stem,
                    'ext': self.path.suffix}
    
    """ returns a path from start directory to stop directory, inclusive.
        useful for building paths to subdirectories in the EAGLE folder 
        to read/write files from other places, provided the structure of self.nest is used. 
        talon can be any child directory of the EAGLE folder.
        ex: ./EAGLE/projects/adventure/pedals/dreamReaper/v1_4/dreamReaperV1_4Panel2X2.brd
            ./EAGLE/BOMs/onederEffects/pedals/redRyder/v1_2/redRyderV1_2Bom.txt
            ./EAGLE/pickAndPlace/adventure/eurorack/merge/v1_5/mergeV1_5Panel.dpv"""
    def getPath(self, start, stop):
        dirKeys = list(self.nest.keys())
        getKeys = dirKeys[dirKeys.index(start):dirKeys.index(stop)+1]
        path = pathlib.Path(*[self.nest[key] for key in getKeys if key != 'ext'])
        return path.with_suffix(self.nest['ext']) if stop == 'ext' else path




