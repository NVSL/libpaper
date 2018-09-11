#!/bin/bash
PAPER=2019FAST_Orion
SED=s/CURRENTGITCOMMIT/$*\/g
SAVED_PWD=`pwd`

# TODO add .lock
cd ../$PAPER
git pull
git checkout master
git checkout $1
echo cmdline: $* >> $SAVED_PWD/build.log
echo sed: $SED >> $SAVED_PWD/build.log
sed -i "$SED" paper.tex
make clean
make
gsutil cp paper.pdf gs://jian-storage/paper.pdf
git reset --hard
