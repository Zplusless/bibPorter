## New plan

1. 写作时候仅插入bibkey，可以用快速拷贝，也可以用cite as you write的API，详见https://retorque.re/zotero-better-bibtex/citing/cayw/
2. bibPorter变量tex文件，利用pull export的API拉取全部bib，详见https://retorque.re/zotero-better-bibtex/exporting/pull/
3. 从全部bib中筛选出需要的，生成.bib文件
4. 对bib文件中的entity进行检查，筛选遗漏项目，整理缩写等， 参考http://abbrv.jabref.org/  https://blog.csdn.net/OpenSourceSDR/article/details/51907111





# Plan-A

## 1. bib insert

变写边插入，从图形界面选择文献后，将bib条目追加到指定bib文件中，并在当前文件中插入key

## 2. bib check

>  1. 检查bib文件中各个条目是否格式正确
>  2. 是否缺项目
>  3. 作者是否为全名
>  4. 是否包含in proceedings of 

## 3. bib generate

遍历.tex文件，将其中所有\cite{}中的key找出，并生成一份对应的bib文件

## 4. 图形界面

类似zotero的word插件的界面

## 5. 通知栏图标常驻



# Plan-B

1. 利用zotero自动导出全文献至指定路径
2. 写作时仅导入bibkey
3. 在传统的编译前加入bibPorter命令，遍历全文，找出所有的bibkey，并将对应的文献内容贴到当前路径下的指定bib文件中
4. bib文件名能从`\bibliography{IEEEabrv,reference}`命令中自动识别
5. 可以利用texstudio的自定义命令功能，做成新的快捷键
