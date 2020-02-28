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

def modify_bibs(bib_str:str):
    biblines = bib_str.split('\n')

    for i, line in enumerate(biblines):
        if 'month' in line:
            biblines[i] = modify_month(line)

    return '\n'.join(biblines)

# 待增加bibkey遍历功能
def get_bibinfo(texfile:str):
    '''
    遍历tex文件，返回bibkey的列表和tex文件中指向的bib文件
    bib文件名由 \bibliography{reference} 命令确定
    '''
    bibkeys=[]
    bibfile=''
    
    with open(texfile, 'r', encoding='utf8') as tf:
        lines = tf.readlines()

    jump_line = False #标记跨行的cite引用
    for line in lines:
        # 查找cite key
        if r'\cite' in line:
            # print(line, end='')
            re_item = re.match(r'[^%]*\\cite\{(.*)\}.*', line)
            if re_item:
                keys = re_item.group(1).replace(' ','').split(',')    
                # print(keys, '\n')
                bibkeys.extend(keys)
            else:
                re_item = re.match(r'[^%]*\\cite\{(.*)$', line) 
                if re_item:
                    jump_line=True # 后面有跨行的key
                    keys = re_item.group(1).replace(' ','').replace('\n','').replace('\r','').split(',')
                    # print(keys, '\n')
                    bibkeys.extend(keys)
                    continue # 本行处理完，进入下一行，处理跨行的key
                else:
                    raise Exception('跨行匹配错误')
        if jump_line:
            if '}' in line:
                jump_line = False
                re_item = re.match(r'^([^%]*)\}.*', line) 
                if re_item:
                    keys = re_item.group(1).replace(' ','').replace('\n','').replace('\r','').split(',') 
                    # print(keys, '\n')
                    bibkeys.extend(keys)
            else: #不含}的跨行，只包含key
                re_item = re.match(r'([^%]*)%?.*', line)
                keys = re_item.group(1).replace(' ','').replace('\n','').replace('\r','').split(',')  
                # print(keys)
                bibkeys.extend(keys)

        # 查找bib文件名
        re_item=re.match(r'^\\bibliography\{(.*)\}', line)
        if re_item:
            bibfile=re_item.group(1)+'.bib'

    bibkeys = set(bibkeys)    
    if '' in bibkeys:
        bibkeys.remove('')
    return bibkeys, bibfile

# 找到tex文件
def get_tex_file(path:str):
    dir_list = os.listdir(path)
    no_match = True
    for file in dir_list:
        if os.path.splitext(file)[1] == ".tex":
            no_match = False
            return file  # 返回tex文件名字
    if no_match:
        raise FileNotFoundError('no tex file at ----> '+path)

if __name__ == "__main__":
    texfile='test/ieee/main.tex'
    bibkeys, bibfile = get_bibinfo(texfile)
    print('\n\n\n\n==========\n', bibkeys, bibfile)
    get_tex_file('test/')