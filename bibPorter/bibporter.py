import bibtexparser as bp
import os
import argparse
from util import modify_bib, get_bibinfo, get_tex_file
from gooey import Gooey, GooeyParser
import json
import sys


# 直接输出，避免stdout被python缓存---->Gooey用pyinstaller打包的要求
# nonbuffered_stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
# sys.stdout = nonbuffered_stdout


@Gooey(program_name='BibPorter')
def main():

    # 读取配置文件
    local_dir =  os.getcwd() # 指定tex源文件的路径
    config_file = os.path.join(local_dir, 'bibporter_config.json')
    config_dict = {}
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf8') as f:
            config_dict = json.load(f)
    else:
        config_dict['input'] = None
        config_dict['tex'] = None
        config_dict['output'] = None
        config_dict['config'] = 'no'

    # parser = argparse.ArgumentParser()
    parser=GooeyParser(description='Pick bib keys from .tex file and generate bib file')
    parser.add_argument('input', 
                        help='the path of origin bib file expoted by zotero', 
                        default=config_dict['input'], 
                        widget="FileChooser")
    parser.add_argument('-t', '--tex', 
                        help='the path of tex file', 
                        default=config_dict['tex'], 
                        widget="FileChooser")
    parser.add_argument('-o', '--output', 
                        help='the path of bib file you are using for latex. By default the current path', 
                        default = config_dict['output'],
                        widget="DirChooser")
    parser.add_argument("config",                        
                        help="remember the config, if no, the config file will be deleted", 
                        # action="store_true", 
                        # widget='CheckBox',
                        choices = ['yes', 'no'],
                        default=config_dict['config'])
    args = parser.parse_args()


    # 如果确认写入配置
    if args.config == 'yes':
        with open(config_file, 'w', encoding='utf8') as f:
            config_dict['input'] = args.input
            config_dict['tex'] = args.tex
            config_dict['output'] = args.output
            config_dict['config'] = args.config
            json.dump(config_dict, f)
            print('Configure has been writen into: \n{}'.format(config_file), '\n===========================')
    else:
        if os.path.exists(config_file):
            os.remove(config_file)
            print('Configure file has been deleted', '\n===========================')
            
    # print(type(args))
    
    originfile = modify_bib(args.input) # 将zotero输出的源文件修改，改变月份
    tex_file = args.tex if args.tex else os.path.join(local_dir, get_tex_file(local_dir))   # 如未给出，则在当前路径中寻找tex文件
    bib_keys, bib_name = get_bibinfo(tex_file)  # 获取bibkey和bib文件
    tex_dir, _ = os.path.split(tex_file)    # 分离texfile的路径和文件
    bib_name = os.path.join(tex_dir, bib_name) # 拼接路径，指向tex相同路径下
    output_bib = args.output if args.output else bib_name   # 有命令行参数则选为参数，否则使用tex文件中指定的名称，放在相同路径下


    # 从修改过的bib文件中载入，用于处理
    with open(originfile, encoding='utf8') as b_file:
        bibdata = bp.load(b_file)

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

    # print(bibdata_out)
    with open(output_bib, 'w', encoding='utf8') as bib_write:
        bp.dump(bibdata_out, bib_write)


if __name__ == "__main__":
    main()

