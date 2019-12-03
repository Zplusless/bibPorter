import bibtexparser as bp
import os
from util import *

originfile = '../bib/test.bib'
bibfile = originfile.replace('.bib','_modified.bib')


cwd = os.getcwd()
print('当前路径：'+cwd)

with open(bibfile, encoding='utf8') as b_file:
    bibdata = bp.load(b_file)

print(bibdata.entries)

for d in bibdata.entries:
    if 'file' in d.keys():
        del d['file']
    if 'keywords' in d.keys():
        del d['keywords']

with open(bibfile.replace('modified', 'pro'), 'w', encoding='utf8') as bib_write:
    bp.dump(bibdata, bib_write)
