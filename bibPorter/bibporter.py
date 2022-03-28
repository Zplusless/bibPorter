import bibtexparser as bp
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import UndefinedString
import os
import argparse
from util import modify_bibs, get_bibinfo, get_tex_file, check_entity
import requests
import sys
import io
import re

# 强制设置输出编码
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

ZOTERO_API='http://127.0.0.1:23119/better-bibtex/library?/1/library.bibtex'

def main():

    local_dir =  os.getcwd() # 指定tex源文件的路径

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tex', 
                        help='the path of tex file')
    parser.add_argument('-o', '--output', 
                        help='the path of bib file you are using for latex. By default the current path')
    parser.add_argument('-e', '--exclude',
                        help='a bib file in which the bibkeys will not be parsed from zotero, using reference_fix.bib by default')
    args = parser.parse_args()

    
    tex_files = args.tex.replace(' ', '').split(',') if args.tex else [os.path.join(local_dir, f) for f in get_tex_file(local_dir) ]  # 如未给出, 则在当前路径中寻找tex文件
    bib_keys = []
    bib_name = None  # todo 不能处理多个bib_name,不过一般不存在这种情况, 只有main.tex中会有这个命令
    for f in tex_files:
        key, temp_name = get_bibinfo(f)  # 获取bibkey和bib文件
        bib_keys.extend(key)
        if temp_name:  # ! # bug 此处bib_dir应该有bug,中文情况下split出来的路径有问题 
            bib_name = temp_name
            # bib_dir = os.path.split(f)
    
    if not bib_name:
        print('bib file name not found, using reference.bib by default')
        bib_name = 'reference.bib'
    
    tex_dir = os.path.split(args.tex)[0] if args.tex else local_dir    # 分离texfile的路径和文件
    bib_name = os.path.join(tex_dir, bib_name) # 拼接路径, 指向tex相同路径下
    output_bib = args.output if args.output else bib_name   # 有命令行参数则选为参数, 否则使用tex文件中指定的名称, 放在相同路径下


    # 从zotero的API中读取数据
    try:
        r = requests.get(ZOTERO_API)
    except requests.exceptions.ConnectionError:
        print('zotero is not working, get bib data failed')
        sys.exit(1)
    if r.status_code == 200:
        print('get zotero data success!')
    else:
        raise Exception('fail to get data from zotero, status code: {}'.format(r.status_code))
        sys.exit(1)
    r.encoding = 'utf-8'
    bib_str = modify_bibs(r.text)

    # with open('./bib_str.txt', 'w', encoding='utf8') as out_bib:
    #     out_bib.write(bib_str)


    # 构建BibtexParser
    bibParser = BibTexParser(common_strings=False)
    bibParser.ignore_nonstandard_types = True
    bibParser.homogenise_fields = True
    bibdata = bp.loads(bib_str, bibParser)

    # for i in range(100,120):
    #     print(bibdata.entries[i])
    #     print(type(bibdata.entries[i]), '\n')

    # 对bib库进行格式处理
    # 此处效率低, 应该直接从大库里读bib id, 存在则append, 否则, 报错
    bibdata_out = bp.bibdatabase.BibDatabase()

    num_all = len(bib_keys)



    # 检查导入失败的是否在被引用的其它bib文件里
    excluded_keys = set()
    exclude_file = args.exclude if args.exclude else "reference_fix.bib"
    exclude_file_path = os.path.join(tex_dir, exclude_file)
    with open(exclude_file_path) as ex_f:
        try:
            exclude_data = bp.load(ex_f)
        except UndefinedString as e:
            print(f'\n\033[31mError ====> {exclude_file} has undefined String：{e} \033[0m')
            exit(-1)


    for d in exclude_data.entries:
        if d['ID'] in bib_keys:
            try:
                # excluded_keys.add(d['ID'])
                bibdata_out.entries.append(d)
                entity_check = check_entity(d)
                entity_check_consequence = '---->title: '+ re.sub(r'[{}]','', d['title']) +'\n\t\t|--->missing item: '+ str(entity_check) if entity_check else ''
                print('Excluded---->'+d['ID'], entity_check_consequence)
                while d['ID'] in bib_keys:
                    bib_keys.remove(d['ID'])
            except Exception as e:
                print(f"\n\nError article --->  {d['ID']}\n")
                raise e

    print('--------------------\n\n')


    # 爬取剩下没有在exclude_file中的bibkey
    for d in bibdata.entries:
        if d['ID'] in bib_keys:
            try:
                bibdata_out.entries.append(d)
                entity_check = check_entity(d)
                entity_check_consequence = '---->title: '+ re.sub(r'[{}]','', d['title']) +'\n\t\t|--->missing item: '+ str(entity_check) if entity_check else ''
                print('Success---->'+d['ID'], entity_check_consequence)
                while d['ID'] in bib_keys:
                    bib_keys.remove(d['ID'])
            except Exception as e:
                print(f"\n\nError article --->  {d['ID']}\n")
                raise e


    print('--------------------\n\n')




    
    bibkey_not_found = '\n'.join(bib_keys)
    num_not_found = len(bib_keys)
    print('fail to get bibkeys (total {}): \n'.format(num_not_found), bibkey_not_found)
    print('------------end---------------')

    print('Success: {}, Fail: {}'.format(num_all-num_not_found, num_not_found))

    # print(bibdata_out)
    with open(output_bib, 'w', encoding='utf8') as bib_write:
        bp.dump(bibdata_out, bib_write)


if __name__ == "__main__":
    main()

