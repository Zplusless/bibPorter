import bibtexparser as bp
import os
import re

bibfile='../test/test.bib'

def modify_month(bibfile):
    with open(bibfile, encoding='utf8') as bf:
        biblines = bf.readlines()
    for line in biblines:
        if 'month' in line:
            re_item = re.match(' *month *= *([a-zA-Z]*)', line)
            if re_item:    
                print(line)
                month = re_item.group(1)
                print(month)
                line=line.replace(month, '{'+month+'}')
                print(line)
            else:
                print(line.strip('\n')+'<----')

modify_month(bibfile)



# cwd = os.getcwd()
# print('当前路径：'+cwd)

# with open('../test/test.bib', encoding='utf8') as bibfile:
#     bibdata = bp.load()

# print(bibdata.entries)