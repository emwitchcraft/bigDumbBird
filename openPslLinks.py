import webbrowser
import partsSourceList
import sys

browser = webbrowser.get()

pslFile = sys.argv[1] if len(sys.argv) > 1 else input('gimme file:')

pslReader = partsSourceList.PartsSourceListReader(pslFile)
#browser.open_new('https://arrow.com')
for i,item in enumerate(pslReader.parts.sections()):
    if i > 0:# and r'%' not in pslReader.parts[item]['link']:
        try:
            browser.open_new_tab(pslReader.parts[item]['link'])
            input()
        except:
            print(f'couldnt open {pslReader.parts[item]["link"]}')