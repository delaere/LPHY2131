#!/bin/env sh

git clone https://github.com/delaere/LPHY2131.wiki.git
cd LPHY2131.wiki
for i in *.md; { pandoc -f markdown_github -t latex --base-header-level=2 $i -o `basename $i .md`.tex; }
for i in *.tex; { sed -i.bak -e 's/verbatim/myverb/' $i; }
cp ../LPHY2131_Documentation.tex .
pdflatex LPHY2131_Documentation.tex
pdflatex LPHY2131_Documentation.tex
cp LPHY2131_Documentation.pdf ..
cd ..
rm -rf LPHY2131.wiki

