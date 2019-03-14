#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys
import time
from datetime import timedelta
from sklearn.neighbors import BallTree


def balltree(data,size=50):
   tree = BallTree(data,leaf_size=size) 
   return tree
