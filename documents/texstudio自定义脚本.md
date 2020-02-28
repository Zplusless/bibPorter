As with most things latex, it is a bit more complicated than with word/libre office, but not very difficult.

If you use the better biblatex plugin in zotero (https://retorque.re/zotero-better-bibtex/), you can auto export your library to a bib-file. Many latex-editors are able to auto-complete citation-keys from your bib-file and show you some information from the citation.

I use texstudio and when I write a citation, \autocite{, it pops up a list of citation keys with the text from the bib-file like this: https://www.dropbox.com/s/5jqvapg9vul1jys/Screenshot 2018-04-03 10.07.20.png?dl=0

Texstudio is also customizable through macros, and I've made my own citation macro which I have bound to ctrl + <. When I press this key-combination I get the text \autocite{} or \textcite{} and it shows my citation keys like above.

To make the macro you have to choose "script" and the macro is:

```coffeescript
%SCRIPT
editor.write("\\autocite{}");
cursor.shift(-1);
app.normalCompletion()
```

