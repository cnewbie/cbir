#!/usr/bin/env python
#-*- coding:utf-8 -*-

import numpy as np
from skimage.feature import local_binary_pattern
import cv2
import sys

class LBPDescriptor:
    def __init__(self,num_points=8,radius=1,method='default'):
        self.num_points=num_points
        self.radius=radius
        self.method=method
    def describe(self,image):
        if self.method == 'uniform':
            gbins=self.num_points+2
        elif self.method == 'var':
            gbins=2**(self.num_points+1)
        else:
            gbins=2**self.num_points
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #uniform method return num_points+2 dimension histogram
        lbp_img = local_binary_pattern(image, self.num_points, self.radius, self.method)
        #get all histogram by sliding window
        hist=np.empty(0)
        (winW,winH)=(32,32)
        def _sliding_window(image,step,window_size):
            for y in range(0,image.shape[0],step):
                for x in range(0,image.shape[1],step):
                    yield (x,y,image[y:y+window_size[1],x:x+window_size[0]])
        def _normalize(v):
            norm=np.linalg.norm(v, ord=1)
            if norm==0:
                norm=np.finfo(v.dtype).eps
            return v/norm
        for (x,y,window) in _sliding_window(lbp_img,step=32,window_size=(winW,winH)):
            if window.shape[0] != winH or window.shape[1] != winW:
                #raise ValueError('window size is not suitable for sliding window')
                #print('size miss match %d - %d'% (window.shape[0],winH))
                pass
            window_hist,bins_=np.histogram(window,bins=gbins,range=(0,gbins),density=False)
            window_hist=_normalize(window_hist)
            hist=np.concatenate((hist,window_hist))
        # hist,bins=np.histogram(hist,bins=gbins,range=(0,gbins))
        # print(hist.shape)
        # print(lbp_img.max(),lbp_img.min())
        # print(sum(hist))
        # print(type(hist))
        hist = _normalize(hist).astype('f')
        return hist
def _test(argv=sys.argv):
    if len(sys.argv) > 1:
        # _hsvd = LBPDescriptor(method='default')
        # _hsvd = LBPDescriptor(method='ror')
        _hsvd = LBPDescriptor(method='uniform')
        # _hsvd = LBPDescriptor(method='var')
        # _hsvd = LBPDescriptor(num_points = 16,radius=2,method='ror')
        # _hsvd = LBPDescriptor(num_points = 16,radius=2,method='uniform')
        _f = _hsvd.describe(cv2.imread(sys.argv[1]))
        print("features : %s\t%s %s\n" % (_f[:16],_f.shape,_f.dtype))
    else:
        print("Usage: %s image"% (__file__,))

if __name__ == "__main__":
    sys.exit(_test())
