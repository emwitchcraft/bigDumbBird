import xml.etree.ElementTree as et

tree = et.parse ('C:/users/machew/documents/eagle/projects/pnpTestBoard/PNPOrientationTestBoard.brd')
#tree = et.parse ('test.xml')

root = tree.getroot ()
""" print (root)
print (len (root))
for s in root: print (s)
sub1 = root.findall ('./')
for s in sub1: 
    print (s)
    sub2 = s.findall ('./')
    print (len (sub2)) """
#for s in sub2: print (s)
""" for item in root.findall ('./'):
    print (item.text)
    for subitem in item:
        print (subitem.text) """
        
def getTreeStructure (root):
    return 0

def getElemStructure (elem, layer=0):
    tags = []
    for sub in elem:
        tags.append ((sub.tag, layer))
        if len (sub) > 0:
            tags.extend (getElemStructure (sub, layer + 1))
    return tags
    
def getTags (elem):
    return [sub.tag for sub in elem.findall ('./')]

#print (getTags (root))
""" print ()
for sub in root.iter ():
    print (sub)
    
print ()
for sub in root.iterfind ('./'):
    print (sub)
    """
print ()
for sub in root:
    print (sub)
    for sub2 in sub:
        print (sub2)
        for sub3 in sub2:
            print (sub3)

structure = getElemStructure (root)
tab = '  '
with open ('eagleBoardFileTagStructure.txt', 'w') as file:
    file.writelines ([tab * s[1] + 'l' + str (s[1]) + ': ' + str (s[0] + '\n') for s in structure])