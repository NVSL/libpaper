#!/bin/bash
PAPER_ROOT="$HOME/papers"
PAPER=$1
GS_BUCKET="gs://libpaper-autobuild" # Don't add /
SAVED_PWD=`pwd`

buildonce()
{
    git pull
    make clean
    make
    echo $GS_BUCKET/$PAPER
    gsutil cp *.pdf $GS_BUCKET/$PAPER/
    gsutil cp paper.pdf $GS_BUCKET/$PAPER.pdf
}

cd $PAPER_ROOT

if [ ! -d $PAPER ]; then
	echo "Cloning repo $PAPER."
	git clone git@github.com:NVSL/$PAPER.git
	(cd $PAPER && make)
fi

cd $PAPER_ROOT/$PAPER
echo cmdline: $* >> $SAVED_PWD/build.log

# Tag rebuild when the paper is being built
if [ -f .build ]; then
	touch .rebuild
	return 0
fi

touch .build
buildonce

while [ -f .rebuild ]; do
	rm -f .rebuild
	buildonce
done

rm .build -f
