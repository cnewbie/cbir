#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import cv2
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances_argmin
#from .sift import SIFTDescriptor
from apps.features import (sift,orb,surf)

_mode_len={'sift':128,'surf':64,'orb':32}
class VLADDescriptor:
    def __init__(self,visual_dict,mode):
        self.visual_dict = visual_dict
        self.vlad_mode = mode
        self.len = _mode_len.get(mode)*visual_dict.shape[0] 

    def _get_vlad(self,X): 
        if X is not None:
            centers = self.visual_dict
            if X.shape[1] == centers.shape[1]:
                predict_labels = pairwise_distances_argmin(X,centers)
                num = centers.shape[0]
                rows,cols = X.shape
                V=np.zeros([num,cols])
                for i in range(num):
                    if np.sum(predict_labels==i)>0:
                        V[i] = np.sum(X[predict_labels==i,:]-centers[i],axis=0)
                V = np.nan_to_num(V.ravel())
                V = np.sign(V)*np.sqrt(np.abs(V))
                V = V/np.sqrt(np.dot(V,V))
                V = (V*10**6).astype('i')
                return V
            else:
                raise ValueError("features and coding mode mismatch")
        else:
            return None
    def describe(self,image):
        if self.vlad_mode == 'sift':
            descriptor = sift.SIFTDescriptor()
        elif self.vlad_mode == 'surf':
            descriptor = surf.SURFDescriptor()
        elif self.vlad_mode == 'orb':
            descriptor = orb.ORBDescriptor()
        kps,des = descriptor.describe(image)
        results = self._get_vlad(des)
        return results

