#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from sklearn.cluster import MiniBatchKMeans

'''
    kmeas wrapper

    Args:
        data: data need to be cluster
        num: Optinal variable , num of center of cluster
        tol: tolerance
        debug: debug switch
    Returns:
        array
'''

def kmeans_dict(data,num=256,tol=0,debug=False):
    batch_num = 300
    if len(data.shape) < 2:
        raise ValueError("numpy array must be 2 dimension")
    samples_num = data.shape[0]
    cnt = samples_num // batch_num
    kmeans_ = MiniBatchKMeans(n_clusters=num,max_iter=300,batch_size=batch_num,n_init=num,tol=tol,verbose=debug)
    for i in range(cnt):
        if i+batch_num <= samples_num:
            kmeans_.partial_fit(data[i:i+batch_num])
        else:
            kmeans_.partial_fit(data[i:samples_num])
    return kmeans_.cluster_centers_
