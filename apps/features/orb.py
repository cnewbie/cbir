#!/usr/bin/env python
# -*- coding;utf-8 -*-

import cv2
import sys 

class ORBDescriptor:
    def __init__(self,nfeatures=1000):
        self.num_features=nfeatures

    def describe(self,image):
        if(len(image.shape) == 3):
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        orb_ = cv2.ORB_create(self.num_features)
        kps,des = orb_.detectAndCompute(image,None)
        return kps,des

