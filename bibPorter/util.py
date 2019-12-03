import os
import re


def modify_month(line:str):
    re_item = re.match(' *month *= *([a-zA-Z]*)', line)
    if re_item:    
        month = re_item.group(1)
        line=line.replace(month, '{'+month+'}')
        return line

def modify_bib(bibfile):
    with open(bibfile, encoding='utf8') as bf:
        biblines = bf.readlines()
        for i, line in enumerate(biblines):
            if 'month' in line:
                biblines[i] = modify_month(line)
    
    with open(bibfile.replace('.bib', '_modified.bib'), 'w', encoding='utf8') as bf_out:
        bf_out.writelines(biblines)

if __name__ == "__main__":
    bibfile='../bib/test.bib'
    modify_bib(bibfile)