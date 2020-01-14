import os
import re


def modify_month(line:str):
    re_item = re.match(' *month *= *([a-zA-Z]*)', line)
    if re_item:    
        month = re_item.group(1)
        line=line.replace(month, '{'+month+'}')
        return line

def modify_bib(bibfile):
    outputfile=bibfile.replace('.bib', '_modified.bib')
    
    with open(bibfile, encoding='utf8') as bf:
        biblines = bf.readlines()
        for i, line in enumerate(biblines):
            if 'month' in line:
                biblines[i] = modify_month(line)
    
    with open(outputfile, 'w', encoding='utf8') as bf_out:
        bf_out.writelines(biblines)

    return outputfile

# 待增加bibkey遍历功能
def get_bibkeys(texfile:str):
    '''
    遍历tex文件，返回bibkey的列表和tex文件中指向的bib文件
    bib文件名由 \bibliography{reference} 命令确定
    '''
    bibkeys=[]
    bibfile=''
    
    return bibkeys, bibfile


if __name__ == "__main__":
    bibfile='../bib/test.bib'
    modify_bib(bibfile)