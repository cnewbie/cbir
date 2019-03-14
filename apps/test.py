#!/usr/bin/env python
# -*- utf-8 -*-

import os
import sys
import cv2
import numpy as np
import argparse
import logging
import logging.config
if __name__ == "__main__":
    sys.path.append('../')
from matplotlib import pyplot as plt
from apps.features import (sift,vlad,orb,surf)
from apps.utils import (fileutils)
from apps import searcher 


def test_sift(img):
    sift_ = sift.SIFTDescriptor()
    kps,des = sift_.describe(img)
    return des.astype('i')
    print(des.shape,des.dtype,des[0])
def test_surf(img):
    surf_ = surf.SURFDescriptor()
    kps,des = surf_.describe(img)
    print(des.shape,des.dtype,des[0])
def test_orb(img):
    orb_ = orb.ORBDescriptor()
    kps,des = orb_.describe(img)
    print(des.shape,des.dtype,des[0])
def test_vlad(img):
    a=np.ones([12,128])
    b=np.ones([12,64])
    c=np.ones([12,32])
    vlad_a = vlad.VLADDescriptor(a,'sift')
    res_a = vlad_a.describe(img)
    vlad_b = vlad.VLADDescriptor(b,'surf')
    res_b = vlad_b.describe(img)
    vlad_c = vlad.VLADDescriptor(c,'orb')
    res_c = vlad_c.describe(img)
    vlad_d = vlad.VLADDescriptor(c,'surf')
    #res_d = vlad_d.describe(img)
    print(res_a.shape,res_a.dtype,res_a[:128])
    print(res_b.shape,res_b.dtype,res_b[:64])
    print(res_c.shape,res_c.dtype,res_c[:32])
    
def test_fileutils(file_path):
    res = fileutils.filelist(file_path)
    print(len(res),res[:32])

def test_searcher(img,mode,dis_mode,type_):
    searcher_ = searcher.Searcher()
    if type_ == 1:
        res = searcher_.search(img,mode=mode,dis_mode=dis_mode,limit=12)
    elif type_ ==2:
        res = searcher_.search2(img,mode=mode,limit=12)
    #print(len(res))
    #print(res)

    fig=plt.figure(figsize=(12, 6))
    query_plot=plt.subplot(4,4,1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    query_plot.imshow(img)
    plt.title('query image')
    query_plot.axis('off')
    for i,img_res in enumerate(res):
        plot_=plt.subplot(4,4,i+5)
        img = cv2.cvtColor(cv2.imread(img_res[0]), cv2.COLOR_BGR2RGB)
        plot_.imshow(img)
        plot_.set_xticks([])
        plot_.set_yticks([])
        #plt.title("{:7f}".format(img_res[1]))
        plt.title("{}".format(os.path.basename(img_res[0])))
        plot_.axis('off') 
    plt.show()

def test(argv=sys.argv):
    parser = argparse.ArgumentParser(description='Test Function.')
    parser.add_argument("-i","--input",required=True,help="search image path")
    parser.add_argument("-m","--mode",choices=['sift_vlad','surf_vlad','orb_vlad'],help="search mode")
    parser.add_argument("-d","--distance",choices=['euclidean','manhattan','cosine'],help="distance mode")
    parser.add_argument("-t","--type",default=1,type=int,help="search type")
    args = parser.parse_args()
    mode = args.mode
    dis_mode = args.distance
    type_=args.type
    img = cv2.imread(args.input)
    if img is None:
        print("can't find image")
        return 
    a = test_sift(img)
    #print(a.dtype)
    #test_surf(img)
    #test_orb(img)
    #test_vlad(img)
    #test_fileutils(os.path.dirname(_img_path))
    test_searcher(img,mode,dis_mode,type_)
if __name__ == "__main__":
    test()
