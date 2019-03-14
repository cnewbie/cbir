#!/usr/bin/env python
#-*-coding: utf-8 -*-
import sys
import cv2



class SIFTDescriptor:
    def __init__(self,nfeatures=1000):
        self.num_features=nfeatures

    def describe(self,image):
        if(len(image.shape)==3):
            #covert bgr to gray
            image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        sift_=cv2.xfeatures2d.SIFT_create(self.num_features)
        kps,des=sift_.detectAndCompute(image,None)
        return kps,des
