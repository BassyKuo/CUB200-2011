# CUB200-2011

All images from http://www.vision.caltech.edu/visipedia/CUB-200-2011.html

## Steps

1. Download the tgz files of [images](http://www.vision.caltech.edu/visipedia-data/CUB-200-2011/CUB_200_2011.tgz) and [segmentations](http://www.vision.caltech.edu/visipedia-data/CUB-200-2011/segmentations.tgz) link from the official website.

	Or you can use `download.sh` script to do it. Try: 

		$ ./download.sh

	(Before using, make sure you have installed `wget` and `tar` daemon.)


2. Check the following python packages required:
	* os
	* numpy
	* argparse
	* scipy

	Then run `center_crop.py` to process the raw images. For example:
	
		$ python3 center_crop.py -dd <dataset_path> -ii <dataset_path>/images.txt -bb <dataset_path>/bounding_boxes.txt -os '80,80'

	Try `python3 center_crop.py -h` to see more information how to use.

3. All crop-images saved in `<dataset_path>/center_crop/`. You can also see the pair list of crop-images and crop-segmentations in `images_seg.txt`.
