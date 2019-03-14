#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys
import hashlib
import string
import cv2
import numpy as np
import tornado.web
import tornado.escape
#from .features import lbp
from apps.features import lbp
#from apps.utils import searchutils
#from . import searcher
from apps import searcher
import logging,logging.config

static_path='static'
upload_prefix = 'upload'
#index file location
index_file='apps/index.h5'
EXTS = 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG'
#logging.config.fileConfig('apps/logging.conf')
#logger = logging.getLogger('root')
def _get_results(img_path):
    # start_time=time.time()
    if os.path.exists(index_file):
        _se=searchutils.Searcher(index_file)
    # logger.info(index_file)
    # logger.info(img_path)
    if os.path.exists(img_path):
        img=cv2.imread(img_path)
        # if args['mode'] == 'uniform':
            # _lbp = lbp.LBPDescriptor(num_points=16,radius=2,method='uniform')
        # else :
            # _lbp = lbp.LBPDescriptor()
        _lbp = lbp.LBPDescriptor(num_points=16,radius=2,method='uniform')
        query_feature=_lbp.describe(img)
    results=_se.search(query_feature,mode='uniform')
    return results

def _get_results_v2(img_path,mode='sift_vlad'):
    _mode,_code = mode.split('_')
    if os.path.exists(img_path):
        se=searcher.Searcher(index_file=index_file)
        img=cv2.imread(img_path)
        results=se.search(img,mode=mode)
        return results

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        self.render('index.html',err_msg="",imgpath="",lists={})
    def post(self):
        err_msg = ''
        img_path = ''
        debug_flag = self.get_argument("debug", "")
        if debug_flag:
            debug = True
        else:
            debug = False

        if self.request.files:
            f = self.request.files['imgpath'][0]
            rawname = f['filename']
            extension = os.path.splitext(rawname)[1]
            if extension[1:] not in EXTS:
                err_msg = 'wrong file type'
                self.render('index.html', err_msg=err_msg, imgpath=img_path,lists={})
            dstname = hashlib.md5(f['body']).hexdigest()
            dstname += extension
            # dst_full = upload_prefix + dstname
            dst_full = os.path.join(static_path,upload_prefix,dstname)
            # open(dst_full, 'wb').write(f['body'])
            #logger.info(dst_full)
            print(dst_full)
            if not os.path.isfile(dst_full):
                with open(dst_full, 'wb') as save_img:
                    save_img.write(f['body'])
            # phash_alg, index_alg = get_global_vars()
            #results = _get_results(dst_full)
            results = _get_results_v2(dst_full)
            # print(results)
        else:
            err_msg = 'No file is uploaded'
        self.render('index.html', err_msg=err_msg, imgpath=dst_full,lists=results)
class ResultsHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        self.render('results.html',err_msg="",imgpath="",lists={})
    def post(self):
        if self.request.files:
            f = self.request.files['imgpath'][0]
            upload_filename=f['filename']
            dst_full=os.path.join(static_path,upload_prefix,upload_filename)
            extension = os.path.splitext(upload_filename)[1]
            #logger.info(dst_full)
            print(dst_full)
            if extension[1:] not in EXTS:
                err_msg = 'wrong file type'
                self.write(err_msg)
            if not os.path.isfile(dst_full):
                with open(dst_full, 'wb') as save_img:
                    save_img.write(f['body'])
        # print(self.request.arguments)
        # print(self.get_argument('feature-selected'))
        # self.write(tornado.escape.json_encode({'1':2,'2':4,'fuck':90}))
        #results = _get_results(dst_full)
        results = _get_results_v2(dst_full,mode=self.get_argument('feature-selected'))
        self.render('results.html',lists=results)
