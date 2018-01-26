#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 15:19:54 2018

@author: aditya1
"""
import math
import operator
import numpy as np
import matplotlib.pyplot as plt
import cv2

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
collection = client.test_database.coral2
db = []
num = input('Enter the input Image: ')
for x in collection.find():
    db = np.array(x['distances'])

#print db
#print "This is "+str(len(db))
inputImage = db[num]
#print inputImage
distance = np.zeros(1000*72).reshape(1000,72)

distance = abs(db - inputImage)

distanceSum = np.sum(distance,axis=1)
keys = np.arange(len(distanceSum),dtype=int)
#print keys
#print distanceSum

Imagedictionary = dict(zip(keys, distanceSum))
sorted_images = sorted(Imagedictionary.items(), key=operator.itemgetter(1))

#print sorted_images

i = 0;
for key in sorted_images:
    if(i<=20):
        i = i +1
        imageName = str(key[0])+'.jpg'
        print imageName
        cv2.imshow(str(i),cv2.imread(imageName))
    else:
        break;
cv2.waitKey(0)