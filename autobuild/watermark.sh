#!/bin/sh

# ./watermark.sh VAR-LIBPAPER-VERSION VAR-REPO VAR-COMMIT 

if [ -f "paper.pdf" ]; then
  # VAR-BUILT-TIME
  DATE=`date`

  sed -i "s/VAR-LIBPAPER-VERSION/$1/g" _watermark.tex
  sed -i "s/VAR-REPO/$2/g" _watermark.tex
  sed -i "s/VAR-COMMIT/$3/g" _watermark.tex
  sed -i "s/VAR-BUILT-TIME/$DATE/g" _watermark.tex

  pdflatex _watermark.tex
  # pdftk can only stamp on all pages
  #pdftk paper.pdf stamp _watermark.pdf output final.pdf
  cpdf -stamp-on _watermark.pdf paper.pdf 1 -o final.pdf
  cp final.pdf paper.pdf
  rm -f final.pdf _watermark.pdf _logo.pdf
fi
