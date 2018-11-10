#!/bin/bash
PAPER=$1
SAVED_PWD=`pwd`

# TODO add .lock
cd ../$PAPER
git pull
echo cmdline: $* >> $SAVED_PWD/build.log
echo sed: $SED >> $SAVED_PWD/build.log
make clean
make
gsutil cp paper.pdf gs://jian-storage/$1.pdf
#git reset --hard
