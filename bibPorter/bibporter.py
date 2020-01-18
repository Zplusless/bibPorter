import bibtexparser as bp
import os
import argparse
from util import modify_bib, get_bibinfo, get_tex_file

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='the path of origin bib file expoted by zotero', required=True)
parser.add_argument('-o', '--output', help='the path of bib file you are using for latex. If not given, bibPorter will use the file name in .tex file')
parser.add_argument('-t', '--tex', help='the path of tex file')
args = parser.parse_args()

# 将zotero输出的源文件修改，改变月份
originfile = modify_bib(args.input)
# 指定tex源文件的路径
local_dir = os.getcwd()
# print('---->'+local_dir)
tex_file = args.tex if args.tex else os.path.join(local_dir, get_tex_file(local_dir))
# 获取bibkey和bib文件
bib_keys, bib_name = get_bibinfo(tex_file)
# 分离texfile的路径和文件
tex_dir, _ = os.path.split(tex_file)
bib_name = os.path.join(tex_dir, bib_name) # 拼接路径，指向tex相同路径下

# 有命令行参数则选为参数，否则使用tex文件中指定的名称，放在相同路径下
output_bib = args.output if args.output else bib_name

# 从修改过的bib文件中载入，用于处理
with open(originfile, encoding='utf8') as b_file:
    bibdata = bp.load(b_file)

print(bibdata.entries[1])

# 对bib库进行格式处理
bibdata_out = bp.bibdatabase.BibDatabase()
for d in bibdata.entries:
    # if 'file' in d.keys():
    #     del d['file']
    # if 'keywords' in d.keys():
    #     del d['keywords']
    if d['ID'] in bib_keys:
        bibdata_out.entries.append(d)
        print(d['ID'])
        # print(bibdata_out)

print(bibdata_out)
with open(output_bib, 'w', encoding='utf8') as bib_write:
    bp.dump(bibdata_out, bib_write)




# originfile = modify_bib(r'F:\博士学习\1.论文写作\zotero导出完整数据库.bib')