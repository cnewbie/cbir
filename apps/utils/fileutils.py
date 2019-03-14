#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os

# return all image file list of datasetpath
def filelist(dataset_path):
    results=list()
    if os.path.exists(dataset_path) and os.path.isdir(dataset_path):
        valid_images = (".jpg",".jpeg",".bmp",".png")
        for root, dirs, files in os.walk(dataset_path,followlinks=True):
            dirs.sort()
            files.sort()
            for f in files:
                if (not f.startswith('.')) and (f.lower().endswith(valid_images)):
                    # print("file %s" % os.path.join(root,f))
                    results.append(os.path.join(root,f))
    else:
        raise FileNotFoundError
    return results
