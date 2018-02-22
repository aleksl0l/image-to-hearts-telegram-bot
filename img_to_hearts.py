#!/usr/bin/env python3

from PIL import Image
import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.image
from random import shuffle
import sys
import os


def getAverageRGBN(image):
    """
    Given PIL Image, return average value of color as (r, g, b)
    """
    # get image as numpy array
    im = np.array(image)
    # get shape
    w, h, d = im.shape
    # change shape
    im.shape = (w * h, d)
    #mask = np.zeros(im.shape[0], dtype=bool)
    #for i, item in enumerate(im):
    #    mask[i] = (item.tolist() != [0,0,0,0])
    #print(len(mask[mask==True]))
    # get average
    return tuple(np.average(im, axis=0))


def distance(x, y):
    return np.linalg.norm(x - y)

hsize = 10, 10

im = dict()
im_np_arr = dict()

im['black'] = Image.open('/home/alex/Desktop/hearts_vk/hearts/black4.png')
im['blue'] = Image.open('/home/alex/Desktop/hearts_vk/hearts/blue.png')
im['red'] = Image.open('/home/alex/Desktop/hearts_vk/hearts/red.png')
im['purple'] = Image.open('/home/alex/Desktop/hearts_vk/hearts/purple.png')
im['yellow'] = Image.open('/home/alex/Desktop/hearts_vk/hearts/yellow.png')
im['green'] = Image.open('/home/alex/Desktop/hearts_vk/hearts/green.png')

#print(np.array(img).shape)

mean = {'black': np.array([ 29.05,  27.42,  36.87]), 
        'blue': np.array([  20.13,   99.44,  174.79]), 
        'red': np.array([ 162.48,   33.22,   32.08]), 
        'purple': np.array([ 104.5 ,   23.92, 131.09]), 
        'yellow': np.array([ 197.36,  159.94,   40.95]), 
        'green': np.array([  89.02,  134.15,   49.83])}

for key, value in im.items():
    im[key] = im[key].resize((hsize[0], hsize[1]), Image.ANTIALIAS)
    im_np_arr[key] = np.array(im[key])
    #mean[key] = np.array(getAverageRGBN(im[key])[0:3])

print(mean)

imgChange = Image.open(sys.argv[1])
size = list(imgChange.size)
imgChange = imgChange.resize((size[0] - size[0] % hsize[0], size[1] - size[1] % hsize[1]))
size = list(imgChange.size)
print(size)
count_sq = (size[0] // hsize[0], size[1] // hsize[0])

img_array = np.array(imgChange)
size = img_array.shape[0:2]
count_sq = (size[0] // hsize[0], size[1] // hsize[0])

for i in range(count_sq[0]*count_sq[1]):
    s_w, s_h = i % count_sq[0], i // count_sq[0]
    imslice = img_array[s_w*hsize[0]:s_w*hsize[0]+hsize[0], s_h*hsize[1]:s_h*hsize[1]+hsize[1]]
    imslice = imslice.copy()
    w, h, d = imslice.shape
    imslice.shape = (w * h, d)

    slicemean = np.array(tuple(np.average(imslice, axis=0)))

    mindist = float("inf")
    keymin = ""
    for key, value in im.items():
        dist = distance(slicemean, mean[key])
        if (mindist > dist):
            mindist = dist
            keymin = key
    for i in range(hsize[0]):
        for j in range(hsize[1]):
            img_array[s_w*hsize[1]+i][s_h*hsize[1]+j] = im_np_arr[keymin][i][j][0:3]

name = sys.argv[1].split('/')[-1]
Image.fromarray(img_array).save("/home/alex/images/hearted_"+name)
