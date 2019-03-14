#!/usr/bin/env python
#-*-coding:utf-8-*-

import os
import sys
#if __name__ == "__main__":
#    sys.path.append('../')
import cv2
import h5py
import pickle
import time
#import psutil
import numpy as np
from datetime import timedelta
from apps.features import vlad
from scipy.spatial import distance
#from matplotlib import pyplot as plt


_features_file='index.h5'
_tree_file='index.pickle'
class Searcher(object):
    def __init__(self,index_file=_features_file,tree_file=_tree_file):
        self.index_file=index_file
        self.tree_file=tree_file

    def _cal_distance(self,query_feature,all_features,mode='euclidean'):
        distance_mode = {'euclidean':distance.euclidean,'manhattan':distance.cityblock,'cosine':distance.cosine}
        results=list()
        for feature in all_features:
           results.append(distance_mode[mode](query_feature,feature))
        return results

    def search(self,query_img=None,mode='surf_vlad',dis_mode='euclidean',limit=15):
        index_ = h5py.File(self.index_file,'r')
        _mode,_code = mode.split('_')
        _start=time.time()
        img_lists = index_.get(_mode+'_img_lists')[:]
        features_dict = index_.get(_mode+'_features_dict')[:]
        all_features = index_.get(mode)[:]
        print("load features time of {}".format(timedelta(seconds=time.time()-_start)))

        _start = time.time()
        if features_dict is None:
            raise ValueError("can't load features dictionary")

        #if feature_mode == 'uniform':
        #    pass
        #elif feature_mode == 'sift':
        if _code == 'vlad':
            vlad_ = vlad.VLADDescriptor(features_dict,_mode)
            query_feature = vlad_.describe(query_img)
            if query_feature is not None:
                scores = self._cal_distance(query_feature,all_features,mode=dis_mode)
            else:
                return list()
        if scores:
            idx = np.argsort(scores)
            results=list()
            for i in range(limit):
                results.append((img_lists[idx[i]],scores[idx[i]]))
        #results = sorted(results, key=lambda score: score[1])
        index_.close()
        print("total searcher time of {}".format(timedelta(seconds=time.time()-_start)))
        for i in results:
            print('filename:{0[0]}, score:{0[1]} '.format(i))
        return results
    def search2(self,query_img=None,mode='sift_vlad',limit=15):
        index_ = h5py.File(self.index_file,'r')
        _mode,_code = mode.split('_')
        _start=time.time()
        img_lists = index_.get(_mode+'_img_lists')[:]
        features_dict = index_.get(_mode+'_features_dict')[:]
        print("load features dict time of {}".format(timedelta(seconds=time.time()-_start)))
        _start = time.time()
        with open(_mode+'_'+self.tree_file,'rb') as f:
            tree = pickle.load(f)
        print("load tree file time of {}".format(timedelta(seconds=time.time()-_start)))
        
        _start = time.time()
        if _code == 'vlad':
            vlad_ = vlad.VLADDescriptor(features_dict,_mode)
            query_feature = vlad_.describe(query_img)
            if query_feature is not None:
                dist, ind = tree.query(query_feature.reshape(1,-1),k=limit)
                #print(dist)
                #print(ind)
                results = list()
                for idx,i in enumerate(ind.ravel()):
                    results.append((img_lists[i],dist[0][idx]))
        index_.close()
        print("search time of {}".format(timedelta(seconds=time.time()-_start)))
        for i in results:
            print('filename:{0[0]}, score:{0[1]} '.format(i))
        return results
    
def _test():
    #img=cv2.imread('dataset/test/K3034.jpg')
    #se=Searcher()
    #res=se.search(img,limit=12)
    #print(len(res))
    #print(res[0])
    #fig=plt.figure(figsize=(12, 6))
    #query_plot=plt.subplot(4,4,1)
    ##query_plot.imshow(img[:,:,-1])
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #query_plot.imshow(img)
    #plt.title('query image')
    #query_plot.axis('off')
    #for i,img_res in enumerate(res):
    #    plot_=plt.subplot(4,4,i+5)
    #    img = cv2.cvtColor(cv2.imread(img_res[0]), cv2.COLOR_BGR2RGB)
    #    plot_.imshow(img)
    #    plot_.set_xticks([])
    #    plot_.set_yticks([])
    #    #plt.title(str(img_res[1]))
    #    #plot_.axis('off') 
    #plt.show()
    pass
if __name__ == "__main__":
    _test()
