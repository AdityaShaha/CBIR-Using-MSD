#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 13:33:40 2018

@author: aditya1
"""

# importing libraries
import math
import cv2
import numpy as np
import matplotlib.pyplot as plt

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')

Database = np.zeros(1000*72).reshape(1000,72)
for entry in range(1000):
    imagename = str(entry)+'.jpg'
    img = cv2.imread(imagename)
    width, height, channels = img.shape

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    colnum1 = 8   #the quantization number of H 
    colnum2 = 3   #the quantization number of S 
    colnum3 = 3   #the quantization number of V
    VI = 0
    SI = 0
    HI = 0
    QuantizedImage = np.zeros(width*height).reshape(width,height)
    for i in range(width):
        for j in range (height):
            VI = hsv[i, j, 0] * (colnum1 / 360.0)
            if (VI >= colnum1 - 1):
                VI = colnum1 - 1
            SI = hsv[i, j, 1] * (colnum2 / 1.0)
            if (SI >= colnum2 - 1):
                SI = colnum2 - 1;
            HI = hsv[i, j, 2] * (colnum3 / 1.0)
            if (HI >= colnum3 - 1):
                HI = colnum3 - 1
            QuantizedImage[i][j] = (colnum3 * colnum2) * VI + colnum3 * SI + HI


    OrientationImage = np.zeros(width*height).reshape(width,height)
    gxx=gyy=gxy = 0.0
    rh=gh=bh = 0.0
    rv=gv=bv = 0.0
    theta = 0.0
    hsvComponent = np.zeros(3*width*height).reshape(width,height,3)
    num = 6   #the quantization number of edge orientation

    for i in range(width):
        for j in range(height):
            hsvComponent[i, j, 0] = hsv[i, j, 1] * math.cos(hsv[i, j, 0])
            hsvComponent[i, j, 1] = hsv[i, j, 1] * math.sin(hsv[i, j, 0])
            hsvComponent[i, j, 2] = hsv[i, j, 2]
    for i in range(width-2):
        for j in range(height-2):
        
            rh = (hsvComponent[i - 1, j + 1,0] + 2 * hsvComponent[i, j + 1,0] + hsvComponent[i + 1, j + 1,0]) - (hsvComponent[i - 1, j - 1,0] + 2 * hsvComponent[i, j - 1,0] + hsvComponent[i + 1, j - 1,0]);
            gh = (hsvComponent[i - 1, j + 1,1] + 2 * hsvComponent[i, j + 1,1] + hsvComponent[i + 1, j + 1,1]) - (hsvComponent[i - 1, j - 1,1] + 2 * hsvComponent[i, j - 1,1] + hsvComponent[i + 1, j - 1,1]);
            bh = (hsvComponent[i - 1, j + 1,2] + 2 * hsvComponent[i, j + 1,2] + hsvComponent[i + 1, j + 1,2]) - (hsvComponent[i - 1, j - 1,2] + 2 * hsvComponent[i, j - 1,2] + hsvComponent[i + 1, j - 1,2]);
        
            rv = (hsvComponent[i + 1, j - 1,0] + 2 * hsvComponent[i + 1, j,0] + hsvComponent[i + 1, j + 1,0]) - (hsvComponent[i - 1, j - 1,0] + 2 * hsvComponent[i - 1, j,0] + hsvComponent[i - 1, j + 1,0]);
            gv = (hsvComponent[i + 1, j - 1,1] + 2 * hsvComponent[i + 1, j,1] + hsvComponent[i + 1, j + 1,1]) - (hsvComponent[i - 1, j - 1,1] + 2 * hsvComponent[i - 1, j,1] + hsvComponent[i - 1, j + 1,1]);
            bv = (hsvComponent[i + 1, j - 1,2] + 2 * hsvComponent[i + 1, j,2] + hsvComponent[i + 1, j + 1,2]) - (hsvComponent[i - 1, j - 1,2] + 2 * hsvComponent[i - 1, j,2] + hsvComponent[i - 1, j + 1,2]);
        
            gxx = math.sqrt(rh * rh + gh * gh + bh * bh)
            gyy = math.sqrt(rv * rv + gv * gv + bv * bv)
            gxy = rh * rv + gh * gv + bh * bv
        
            theta = (math.acos(gxy / (gxx * gyy + 0.0001)) * 180.0 / math.pi)
        
            OrientationImage[i, j] = (int)(round(theta * num / 180.0))

            if (OrientationImage[i, j] >= num - 1):
                OrientationImage[i, j] = num - 1

    def StructureMaps(OrientationImage,img,wid,hei,Dx,Dy):
        Color = np.zeros(width*height).reshape(width,height)
        for i in range(width/3):
            for j in range(height/3):
                WA = np.zeros(9)
                m = 3 * i + Dx;
                n = 3 * j + Dy;
                WA[0] = OrientationImage[m - 1, n - 1];
                WA[1] = OrientationImage[m - 1, n];
                WA[2] = OrientationImage[m - 1, n + 1];
                WA[3] = OrientationImage[m + 1, n - 1];
                WA[4] = OrientationImage[m + 1, n];
                WA[5] = OrientationImage[m + 1, n + 1];
                WA[6] = OrientationImage[m, n - 1];
                WA[7] = OrientationImage[m, n + 1];
                WA[8] = OrientationImage[m, n];
                if (WA[8] == WA[0]):
                    Color[m - 1, n - 1] = img[m - 1, n - 1]
                else:
                    Color[m - 1, n - 1] = -1
        
                if (WA[8] == WA[1]):
                    Color[m - 1, n] = img[m - 1, n]
                else:
                    Color[m - 1, n] = -1
        
                if (WA[8] == WA[2]):
                    Color[m - 1, n + 1] = img[m - 1, n + 1]
                else:
                    Color[m - 1, n + 1] = -1
        
                if (WA[8] == WA[3]):
                    Color[m + 1, n - 1] = img[m + 1, n - 1]
                else:
                    Color[m + 1, n - 1] = -1
            
                if (WA[8] == WA[4]):
                    Color[m + 1, n] = img[m + 1, n]
                else:
                    Color[m + 1, n] = -1
                if (WA[8] == WA[5]):
                    Color[m + 1, n + 1] = img[m + 1, n + 1]
                else:
                    Color[m + 1, n + 1] = -1
                if (WA[8] == WA[6]):
                    Color[m, n - 1] = img[m, n - 1]
                else:
                    Color[m, n - 1] = -1
                if (WA[8] == WA[7]):
                    Color[m, n + 1] = img[m, n + 1]
                else:
                    Color[m, n + 1] = -1
                if (WA[8] == WA[8]):
                    Color[m, n] = img[m, n]
        return Color

    ColorA = StructureMaps(OrientationImage,QuantizedImage,width,height,0,0)
    ColorB = StructureMaps(OrientationImage,QuantizedImage,width,height,0,1)
    ColorC = StructureMaps(OrientationImage,QuantizedImage,width,height,1,0)
    ColorD = StructureMaps(OrientationImage,QuantizedImage,width,height,1,1)

    micro = np.zeros(width*height).reshape(width,height)
    for i in range(width):
        for j in range(height):
            micro[i][j] = int(max(ColorA[i][j], max(ColorB[i][j], max(ColorC[i][j], ColorD[i][j]))));
    micro = micro.astype(int)

    CSA = 72
    hist = np.zeros(CSA)
    MS = np.zeros(CSA)
    HA = np.zeros(CSA)
    for i in range(width-1):
        for j in range(height-1):
            if(micro[i][j] >= 0):
                HA[micro[i][j]]+=1
            
    for i in range(3,3*(width/3)-1):
        for j in range(3,3*(height/3)-1):
            wa = np.zeros(9)
            wa[0] = micro[i - 1][j - 1]
            wa[1] = micro[i - 1][j]
            wa[2] = micro[i - 1][j + 1]
        
            wa[3] = micro[i + 1][j - 1]
            wa[4] = micro[i + 1][j]
            wa[5] = micro[i + 1][j + 1]
        
            wa[6] = micro[i][j - 1]
            wa[7] = micro[i][j + 1]
            wa[8] = micro[i][j]
            wa = wa.astype(int)
            TE1 = 0
            for m in range(8):
                if ((wa[8] == wa[m]) and (wa[8] >= 0)):
                    TE1 = TE1+1
            if(wa[8]>=0):
                MS[wa[8]] +=TE1
            
    for i in range(CSA):
        hist[i] = (MS[i] * 1.0) / (8.0 * HA[i] + 0.0001)
    Database[entry] = hist
    print("Entered for !"+imagename)
    
collection = client.test_database.coral3
collection.insert({"distances":Database.tolist(),
      "name":'Coral Dataset'})
print Database[0]
