import bibtexparser as bp
from bibtexparser.bparser import BibTexParser
import os
import argparse
from util import modify_bibs, get_bibinfo, get_tex_file
import requests
import json
import sys

ZOTERO_API='http://127.0.0.1:23119/better-bibtex/library?/1/library.bibtex'

def main():

    local_dir =  os.getcwd() # 指定tex源文件的路径

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tex', 
                        help='the path of tex file')
    parser.add_argument('-o', '--output', 
                        help='the path of bib file you are using for latex. By default the current path')
    args = parser.parse_args()

    
    tex_file = args.tex if args.tex else os.path.join(local_dir, get_tex_file(local_dir))   # 如未给出，则在当前路径中寻找tex文件
    bib_keys, bib_name = get_bibinfo(tex_file)  # 获取bibkey和bib文件
    tex_dir, _ = os.path.split(tex_file)    # 分离texfile的路径和文件
    bib_name = os.path.join(tex_dir, bib_name) # 拼接路径，指向tex相同路径下
    output_bib = args.output if args.output else bib_name   # 有命令行参数则选为参数，否则使用tex文件中指定的名称，放在相同路径下


    # 从zotero的API中读取数据
    r = requests.get(ZOTERO_API)
    if r.status_code == 200:
        print('成功从zotero读取数据')
    else:
        raise Exception('未能从zotero读取数据，状态码：{}'.format(r.status_code))
    r.encoding = 'utf-8'
    bib_str = modify_bibs(r.text)


    # 构建BibtexParser
    bibParser = BibTexParser(common_strings=False)
    bibParser.ignore_nonstandard_types = True
    bibParser.homogenise_fields = True
    bibdata = bp.loads(bib_str, bibParser)

    # print(bibdata.entries[1])

    # 对bib库进行格式处理
    # 此处效率低，应该直接从大库里读bib id，存在则append，否则，报错
    bibdata_out = bp.bibdatabase.BibDatabase()
    for d in bibdata.entries:
        if d['ID'] in bib_keys:
            bibdata_out.entries.append(d)
            print('成功导入---->'+d['ID'])
            bib_keys.remove(d['ID'])
    bibkey_not_found = '\n'.join(bib_keys)
    print('以下导入失败：\n', bibkey_not_found)
    print('------------end---------------')

    # print(bibdata_out)
    with open(output_bib, 'w', encoding='utf8') as bib_write:
        bp.dump(bibdata_out, bib_write)


if __name__ == "__main__":
    main()

