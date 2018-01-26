#!/bin/sh

wget http://www.vision.caltech.edu/visipedia-data/CUB-200-2011/CUB_200_2011.tgz
wget http://www.vision.caltech.edu/visipedia-data/CUB-200-2011/segmentations.tgz
wget http://www.vision.caltech.edu/visipedia-data/CUB-200-2011/README.txt

files=$(ls *.tgz --color=no)
for f in $files; do
	tar xvf $f
	rm -i $f
done

mv segmentations CUB_200_2011/
