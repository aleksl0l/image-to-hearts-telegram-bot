#!/usr/bin/env python3

import sys

import numpy as np
from PIL import Image

heart_size = 10, 10
im = {
    'black': Image.open('./hearts/black4.png'),
    'blue': Image.open('./hearts/blue.png'),
    'red': Image.open('./hearts/red.png'),
    'purple': Image.open('./hearts/purple.png'),
    'yellow': Image.open('./hearts/yellow.png'),
    'green': Image.open('./hearts/green.png')
}

mean = {
    'black': np.array([29.05, 27.42, 36.87]),
    'blue': np.array([20.13, 99.44, 174.79]),
    'red': np.array([162.48, 33.22, 32.08]),
    'purple': np.array([104.5, 23.92, 131.09]),
    'yellow': np.array([197.36, 159.94, 40.95]),
    'green': np.array([89.02, 134.15, 49.83])
}


def get_average_rgbn(image):
    image_array = np.array(image)
    w, h, d = image_array.shape
    image_array.shape = (w * h, d)
    return tuple(np.average(image_array, axis=0))


def distance(x, y):
    return np.linalg.norm(x - y)


def img_to_hearts(image):
    im_np_arr = {}

    for key, value in im.items():
        im[key] = im[key].resize((heart_size[0], heart_size[1]), Image.ANTIALIAS)
        im_np_arr[key] = np.array(im[key])
    img_change = image
    size = list(img_change.size)
    img_change = img_change.resize((size[0] - size[0] % heart_size[0],
                                    size[1] - size[1] % heart_size[1]))  # resize image
    size = list(img_change.size)  # new size of image
    print(size)
    # count_sq = (size[0] // hsize[0], size[1] // hsize[0])

    img_array = np.array(img_change)
    size = img_array.shape[0:2]
    count_sq = (size[0] // heart_size[0], size[1] // heart_size[0])  # count segments

    for i in range(count_sq[0] * count_sq[1]):  # loop for all squeres
        s_w, s_h = i % count_sq[0], i // count_sq[0]
        imslice = img_array[s_w * heart_size[0]:s_w * heart_size[0] + heart_size[0], \
                  s_h * heart_size[1]:s_h * heart_size[1] + heart_size[1]]  # copy slice of squre
        imslice = imslice.copy()
        w, h, d = imslice.shape
        imslice.shape = (w * h, d)  # reshape slice for np.average

        slicemean = np.array(tuple(np.average(imslice, axis=0)))

        mindist = float("inf")
        keymin = ""
        for key, value in im.items():  # search what heart is the closest
            dist = distance(slicemean, mean[key])
            if mindist > dist:
                mindist = dist
                keymin = key
        for i in range(heart_size[0]):  # copy heart to image
            for j in range(heart_size[1]):
                if im_np_arr[keymin][i][j][3] > 15:
                    img_array[s_w * heart_size[1] + i][s_h * heart_size[1] + j] = im_np_arr[keymin][i][j][0:3]
    return Image.fromarray(img_array)


if __name__ == '__main__':
    img = Image.open(sys.argv[1])
    img = img_to_hearts(img)
    name = sys.argv[1].split('/')[-1]
    img.save("/home/alex/images/hearted_" + name)
