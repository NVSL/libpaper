#!/bin/bash
PAPER_ROOT="/srv/papers"
PAPER=$1
GS_BUCKET="gs://libpaper-autobuild" # Do not add / in the end
SAVED_PWD=`pwd`
TS=`date +"%Y%0m%0d_%0H%0M%0S"`

buildonce()
{
    git reset --hard # potential conflicts on .last_good_paper_build
    git pull
    make clean
    make
    echo $GS_BUCKET/$PAPER
    gsutil cp *.pdf $GS_BUCKET/$PAPER/
    gsutil cp paper.pdf $GS_BUCKET/$PAPER.pdf
}

mkdir -p $PAPER_ROOT
cd $PAPER_ROOT

if [ ! -d $PAPER ]; then
	echo "Cloning repo $PAPER." >> $SAVED_PWD/build.log
	git clone git@github.com:NVSL/$PAPER.git
	(cd $PAPER && make)
fi

cd $PAPER_ROOT/$PAPER
echo [$TS] $* >> $SAVED_PWD/build.log

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
