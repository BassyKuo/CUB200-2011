# CUB200-2011-crop

All crop images from http://www.vision.caltech.edu/visipedia/CUB-200-2011.html
If the CUB200 dataset is helpful to you, please cite this official website.

## Steps

1. Download the tgz files of [images](http://www.vision.caltech.edu/visipedia-data/CUB-200-2011/CUB_200_2011.tgz) and [segmentations](http://www.vision.caltech.edu/visipedia-data/CUB-200-2011/segmentations.tgz) link from the official website.

	Or you can use `download.sh` script to do it. Try: 

		$ ./download.sh

	(Make sure you have installed `wget` and `tar` before you execute the script.)


2. Extract tgz files to `CUB_200_2011` folder, or any path you want. 

	Now check the following python packages required:
	* os
	* numpy
	* argparse
	* scipy

	and run `center_crop.py` to process the raw images. For example:

		$ python3 center_crop.py -dd CUB_200_2011/ -os '80,80' -od 'center_crop/'

	Try `python3 center_crop.py -h` to see more information how to use.

3. All crop-images and crop-segmentations saved in `<dataset_path>/center_crop/`.
