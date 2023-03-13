# from PIL import Image, ImageOps
import numpy as np
from PIL import Image as im

# img = Image.open('images/test2.jpeg').convert('1')
# img_inverted = ImageOps.invert(img)

# img.save("images/test-bw.jpeg")
# np_img = np.array(img_inverted)
# np_img[np_img > 0] = 1

# print(np_img)

import cv2

"""Convert Image To Binary"""
# read image
img_grey = cv2.imread("images/test2.jpeg", cv2.IMREAD_GRAYSCALE)

# define a threshold, 128 is the middle of black and white in grey scale
thresh = 128

# threshold the image
img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]

# save image
cv2.imwrite("images/bw.jpeg", img_binary)

np_img = np.array(img_binary)
np_img[np_img > 0] = 1
"""Close It"""

print(np_img.shape)

the_array = []

for pix in np_img:
    for pix2 in pix:
        the_array.append(pix2)


data = im.fromarray(the_array)

# saving the final output
# as a PNG file
data.save("images/gfg_dummy_pic.jpeg")


# print(the_array)
