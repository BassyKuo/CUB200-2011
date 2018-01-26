#!/usr/bin/env python3
import os
import numpy as np
import argparse
import scipy.misc

DATA_DIR = '/DATA/CUB_200_2011/'  # change it if you download the dataset in another path

IMAGES_FOLDER = 'images/'
SEGMENTATION_FOLDER = 'segmentations/'
IMAGES_ID_TXT = 'images.txt'
BOUNDING_BOXES_TXT = 'bounding_boxes.txt'

CENTER_CROP_FOLDER = 'center_crop/' # the folder saved center-crop images and segmentations


def make_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dd', '--data_dir', default=DATA_DIR, help='the directory including `images/` and `segmentation/` folder of CUB200_2011 [default: %(default)s]')
    parser.add_argument('-ii', '--images_id', default=os.path.join(DATA_DIR,IMAGES_ID_TXT), help='image id file path [default: %(default)s]')
    parser.add_argument('-bb', '--bounding_boxes', default=os.path.join(DATA_DIR,BOUNDING_BOXES_TXT), help='bounding boxes file path [default: %(default)s]')
    parser.add_argument('-os', '--output_size', default='80,80', help='resize images [default: %(default)s]')
    return parser.parse_args()

if __name__ == '__main__':
    args = make_args()
    output_size = [int(float(n)) for n in args.output_size.split(',')]

    bounding_boxes = {}
    with open(args.images_id, 'r') as f:
        images_id = [line.strip().split(' ') for line in f]
    with open(args.bounding_boxes, 'r') as f:
        for line in f:
            l = line.strip().split(' ')
            bounding_boxes[l[0]] = l[1:]

    #def crop (img, output_size, center=None, scale=None):
        #"""
        #Args
        #- img: np.ndarray. img.shape=[height,width,3].
        #- output_size: tuple or list. output_size=[height, width].
        #- center: tuple or list. center=[x,y].
                  #If cenetr is None, use input image center.
        #- scale: float.
                  #If scale is None, do not scale up the boundary.
        #"""
        #hi,wi = img.shape[:2]
        #ho,wo = output_size
        #x,y = center
        #if scale:
            #ho *= scale
            #wo *= scale
        #print ("ho:", ho)
        #print ("wo:", wo)
        #bound_left  = int(x - wo/2)
        #bound_right = int(x + wo/2)
        #bound_top   = int(y - ho/2)
        #bound_bottom= int(y + ho/2)
        #offset_h = int(y - ho/2)
        #offset_w = int(x - wo/2)
        #return img[offset_h : offset_h + int(ho),
                   #offset_w : offset_w + int(wo)]

    def center_crop (img, output_size, center=None, scale=None):
        """
        Args
        - img: np.ndarray. img.shape=[height,width,3].
        - output_size: tuple or list. output_size=[height, width].
        - center: tuple or list. center=[x,y].
                  If cenetr is None, use input image center.
        - scale: float.
                  If scale is None, do not scale up the boundary.
        """
        hi,wi = img.shape[:2]
        ho,wo = output_size
        if center:
            x,y = center
            if scale:
                ho *= scale
                wo *= scale
                if ho > hi or wo > wi:
                    ho,wo = output_size
            if ho > hi or wo > wi:
                ho = min([hi,wi])
                wo = min([hi,wi])
            bound_left  = int(x - wo/2)
            bound_right = int(x + wo/2)
            bound_top   = int(y - ho/2)
            bound_bottom= int(y + ho/2)

            if bound_left < 0:
                offset_w = 0
            elif bound_right > wi:
                offset_w = int(wi-wo)
            else:
                offset_w = int(x - wo/2)

            if bound_top < 0:
                offset_h = 0
            elif bound_bottom > hi:
                offset_h = int(hi-ho)
            else:
                offset_h = int(y - ho/2)
        else:
            if scale:
                print ("Scaling deny when center variable is None.")
            try:
                if hi < ho and wi < wo:
                    raise ValueError("image is too small. use orginal image.")
            except:
                ho = min([hi,wi])
                wo = ho
            offset_h = int((hi - ho) / 2)
            offset_w = int((wi - wo) / 2)
        return img[offset_h : offset_h + int(ho),
                   offset_w : offset_w + int(wo)]

    cc_dir = os.path.join(args.data_dir, CENTER_CROP_FOLDER)
    cc_img_dir = os.path.join(cc_dir, IMAGES_FOLDER)
    cc_seg_dir = os.path.join(cc_dir, SEGMENTATION_FOLDER)
    try:
        os.makedirs(cc_dir, exist_ok=True)
        os.makedirs(cc_img_dir, exist_ok=True)
        os.makedirs(cc_seg_dir , exist_ok=True)
        print ("Create {} directory.".format(cc_dir))
    except FileExistsError:
        print ("{} directory exists.".format(cc_dir))

    with open(os.path.join(cc_dir, 'images_seg.txt'), 'w') as f:
        for ii in images_id:
            idx, path = ii
            img_path = os.path.join(args.data_dir, IMAGES_FOLDER, path)
            seg_path = os.path.join(args.data_dir, SEGMENTATION_FOLDER, path.replace('.jpg','.png'))
            xmin, ymin, xoffset, yoffset = [float(n) for n in bounding_boxes[idx]]  #xoffset=width, yoffset=height
            center = [int(xmin + xoffset/2), int(ymin + yoffset/2)]
            h = int(max([xoffset, yoffset]))
            for in_path,folder in zip([img_path, seg_path], [IMAGES_FOLDER, SEGMENTATION_FOLDER]):
                name = os.path.join(folder, '{}.{}'.format(idx, in_path.split('.')[-1]))
                img = scipy.misc.imread(in_path)
                _img = center_crop(img, [h,h], center=center, scale=1.2)
                #_img = crop(img, [yoffset, xoffset], center=center)
                try:
                    if _img.shape[2] < 3:   # for segmentation case: _img.shape = [xx,xx,2]
                        _img = _img[:,:,0]
                except IndexError:
                    pass
                _img = scipy.misc.imresize(_img, output_size)
                out_path = os.path.join(cc_dir, name)
                scipy.misc.imsave(out_path, _img)
                print (" -- Save {}".format(out_path))
                f.write("{} ".format(name))
            f.write('\n')

