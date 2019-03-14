#!/usr/bin/env python
#-*- coding:utf-8 -*-
import cv2
import os
import sys
if __name__ == "__main__":
    sys.path.append('../')
import argparse
import time
from datetime import timedelta
#import psutil
import h5py
import pickle
import numpy as np
import logging
import logging.config
#from features import (lbp,vlad,sift,surf,orb)
from features import (vlad,sift,surf,orb)
from utils import (fileutils,dictutils,treeutils)
import configparser

_config_path='config.conf'
#_mem_threshold=50
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('index')
config = configparser.ConfigParser()
config.read(_config_path)
#pid_ = psutil.Process(os.getpid())

def get_files_list(path):
    try:
        _start = time.time()
        image_files=fileutils.filelist(path)
        logger.info("total time of {}".format(timedelta(seconds=time.time()-_start)))
    except FileNotFoundError as e:
        logger.error("dataset must be directory and exists")
    return image_files

def get_all_features(h5f,image_files,mode='sift'):
    mode_len={'sift':128,'surf':64,'orb':32}
    _dataset_name = 'all_'+mode+'_features'
    if h5f.get(_dataset_name) is not None:
        del h5f[_dataset_name]
    f = h5f.create_dataset(_dataset_name,(0,mode_len.get(mode)),maxshape=(None,mode_len.get(mode)))
    if mode == 'sift': 
        descriptor = sift.SIFTDescriptor()
    elif mode == 'surf':
        descriptor = surf.SURFDescriptor()
    elif mode == 'orb':
        descriptor = orb.ORBDescriptor()
    _start = time.time()
    image_lists=list()
    for image_file in image_files:
        img = cv2.imread(image_file)
        kps,des = descriptor.describe(img)
        if des is not None:
            image_lists.append(image_file)
            #all_image_sift_features.append(des)
            old_rows = f.len()
            rows,cols = des.shape
            f.resize(old_rows+rows,axis=0)
            f[old_rows:] = des.astype('f')
            logger.info("extract from {},feature numbers {}".format(os.path.basename(image_file),des.shape[0]))
        else:
            logger.warning("features extract failed {}".format(image_file))
    logger.info("total time of extract {}".format(timedelta(seconds=time.time()-_start)))

    if h5f.get(mode+"_img_lists") is not None:
        del h5f[mode+"_img_lists"]

    imgs_dt = h5py.special_dtype(vlen=str)
    f1 = h5f.create_dataset(mode+'_img_lists',data=np.asarray(image_lists,dtype='O'),dtype=imgs_dt)
    h5f.flush()
    logger.info("dataset size {},img_list size {}".format(f.shape,f1.shape))
    return f 

def get_features_dict(h5f,mode='sift',num='256',debug=True):
    features = h5f.get('all_'+mode+'_features')
    _start=time.time()
    logger.info("start the kmeans")
    features_dict = dictutils.kmeans_dict(features,num=num,debug=debug)
    logger.info("total time of kmeans {}".format(timedelta(seconds=time.time()-_start)))
    if h5f.get(mode+'_features_dict') is not None:
        del h5f[mode+'_features_dict']
    f = h5f.create_dataset(mode+'_features_dict',data=features_dict)
    h5f.flush()
    logger.info('features dict size {}'.format(f.shape))
    return f 

def extract_features(h5f,mode='sift_vlad'):
    _mode,_code = mode.split('_')
    features_dict = h5f.get(_mode+'_features_dict')[:]
    _vlad = vlad.VLADDescriptor(features_dict,_mode)
    if h5f.get(mode) is not None:
        del h5f[mode]
    f = h5f.create_dataset(mode,(0,_vlad.len),maxshape=(None,_vlad.len),dtype='i')
    image_lists = h5f.get(_mode+"_img_lists")[:]
    _start=time.time()
    cnt = 0 
    for image_file in image_lists:
        img = cv2.imread(image_file)
        vlad_result = _vlad.describe(img)
        if vlad_result is not None:
            f.resize(cnt+1,axis=0)
            f[cnt] = vlad_result
            cnt = cnt+1
            logger.info("extract all features from {}".format(os.path.basename(image_file)))
        else:
            logger.warning("{} don't have vlad feature".format(image_file))
    logger.info("total time {}".format(timedelta(seconds=time.time()-_start)))
    logger.info("feature size {}".format(f.shape))
    h5f.flush()
    return f

def index_tree(h5f,leaf_size,mode='sift_vlad'):
    _start = time.time()
    f = h5f.get(mode)
    f_data = f[:]
    tree = treeutils.balltree(f_data,size=leaf_size) 
    logger.info("ball tree time {}".format(timedelta(seconds=time.time()-_start)))
    return tree

def _run(argv =sys.argv):
    parser = argparse.ArgumentParser(description='Index program')
    parser.add_argument("run_type",type=int,help="what to do with dataset?")
    parser.add_argument("-p","--path",default='dataset/train',help="dataset path")
    parser.add_argument("-m","--mode",required=True,choices=['sift_vlad','surf_vlad','orb_vlad'],help="feature extract mode.")
    parser.add_argument("-n","--num",default=256,type=int,help="feature dict number")
    parser.add_argument("-s","--size",default=500,type=int,help="tree leaf size")
    args = parser.parse_args()

    #_start=time.time()
    dataset_path = args.path
    feature_mode = args.mode
    leaf_size = int(args.size)
    dict_num = int(args.num)
    index_file = config['index']['index_file']
    tree_file = config['index']['tree_file']
    _mode,_code = feature_mode.split('_')

    #open index file must exist
    index_ = h5py.File(index_file,'a')
    
    #file list and all features
    if args.run_type == 1 or args.run_type == 0:
        #get all image file name from dataset
        tmp_list=get_files_list(dataset_path)
        #extract all image features 
        dst_ = get_all_features(index_,tmp_list,mode=_mode)
        #print(len(img_lists),dst_.shape)

        #save image file name to file 
        #imgs_dt=h5py.special_dtype(vlen=str)
        #index_.create_dataset(_mode+'_img_lists',data=np.asarray(img_lists,dtype='O'),dtype=imgs_dt)
    #feature dictionary
    if args.run_type == 2 or args.run_type == 0:
        #load_start =time.time()
        #all_features = dst_[:] 
        #print("load total time {}".format(timedelta(seconds=time.time()-load_start)))
        #features_dict = get_features_dict(all_features)
        features_dict = get_features_dict(index_,mode=_mode,num=dict_num)
        #save features dcitionary to file
        #index_.create_dataset(_mode+'_features_dict',data=features_dict)
        features = extract_features(index_,mode=feature_mode)
    #index tree
    if args.run_type == 3 :
        tree = index_tree(index_,leaf_size,mode=feature_mode)
        _start = time.time()
        with open(_mode+'_'+tree_file,'wb') as f:
            pickle.dump(tree,f,protocol=4)
        logger.info("pickle dump time {}".format(timedelta(seconds=time.time()-_start)))
    index_.flush()
    index_.close()
    #logger.info("index total time {}".format(timedelta(seconds=time.time()-_start)))

if __name__ == "__main__":
    sys.exit(_run())
