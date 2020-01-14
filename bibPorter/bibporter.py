import bibtexparser as bp
import os
import argparse
from util import modify_bib

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='the path of origin bib file expoted by zotero', required=True)
parser.add_argument('-o', '--output', help='the path of bib file you are using for latex. If not given, bibPorter will use the file name in .tex file')
args = parser.parse_args()

originfile = modify_bib(args.input)
# originfile = modify_bib(r'F:\博士学习\1.论文写作\zotero导出完整数据库.bib')
bibfile = args.output if args.output else r'G:\0.SyncThing_全局备份\同步代码项目\bibPorter\bib\test.bib'


cwd = os.getcwd()
print('当前路径：'+cwd)

with open(originfile, encoding='utf8') as b_file:
    bibdata = bp.load(b_file)

# print(bibdata.entries)

# 对bib库进行格式处理
for d in bibdata.entries:
    if 'file' in d.keys():
        del d['file']
    if 'keywords' in d.keys():
        del d['keywords']

with open(bibfile, 'w', encoding='utf8') as bib_write:
    bp.dump(bibdata, bib_write)
