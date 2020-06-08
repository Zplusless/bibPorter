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
        if r'%' in line:
            line = line.replace('\%', '_')
            line = line.split('%')[0]  # 利用%分割句子，第一部分就是非注释的部分
            # if line:
            #     print(line)

        # 查找cite key
        if r'\cite' in line:
            no_double_flag = False  # 没有大括号完整的\cite
            no_single_flag = False  # 没有单一大括号的\cite
            
            #  解决所有左右大括号完整的bibkey
            re_items = re.findall(r'\\cite\{([^}]*)\}', line)  # 得到一个list，每个元素是\cite后面大括号内的完整内容
            if re_items: 
                for item in re_items:
                    keys = item.replace(' ','').split(',')    
                    # print(keys, '\n')
                    bibkeys.extend(keys)
            else:
                no_double_flag = True

            # 解决出现在行最后，可能跨行的bibkey
            re_item = re.match(r'[^%]*\\cite\{([^}]*)$', line) # 一定要是[^}],否则可能得到从第一个\cite一直到最后
            if re_item:
                jump_line=True # 后面有跨行的key
                keys = re_item.group(1).replace(' ','').replace('\n','').replace('\r','').split(',')
                # print(keys, '\n')
                bibkeys.extend(keys)
                continue # 本行处理完，进入下一行，处理跨行的key
            else:
                no_single_flag = True
            #两种都没找到，一定有错误
            if no_double_flag and no_single_flag:
                raise Exception(r'在有\cite的行内，未找到bibkey')
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

def check_entity(entity:dict) -> set:
    INPROCEDINGS = {'title', 'booktitle','author', 'year', 'month', 'pages'}
    ARTICLE_JOURNAL = {'title', 'journal', 'author', 'year', 'month', 'volume','pages', 'number'}
    ARTICLE_ARXIV = {'title', 'author', 'year', 'month', 'journal'}
    entity_type = entity['ENTRYTYPE']
    entity_keys = entity.keys()

    # 对于确实缺信息的，在zotero文献的其它一栏写入complete,免去检查
    if 'note' in entity_keys and entity['note'] == 'complete':
        return None 

    if entity_type =='article':
        if 'eprint' in entity_keys or 'arXiv' in entity['journal']:
            return ARTICLE_ARXIV-entity_keys  # 检查arXiv的论文
        else:
            return ARTICLE_JOURNAL-entity_keys # 检查期刊论文
    if entity_type == 'inproceedings':
        return INPROCEDINGS-entity_keys



if __name__ == "__main__":
    texfile='test/ieee/main.tex'
    bibkeys, bibfile = get_bibinfo(texfile)
    print('\n\n\n\n==========\n', bibkeys, bibfile)
    get_tex_file('test/')