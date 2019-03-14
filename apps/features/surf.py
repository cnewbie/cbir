#!/usr/bin/env python
#-*-coding: utf-8 -*-
import sys
import cv2

class SURFDescriptor:
    def __init__(self,n=2000):
        self.threshold=n

    def describe(self,image):
        if len(image.shape) == 3:
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        surf_ = cv2.xfeatures2d.SURF_create(self.threshold)
        kps,des = surf_.detectAndCompute(image,None)
        return kps,des
