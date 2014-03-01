import cv2
import numpy as np


img = cv2.imread('background-image.jpg')
blur = cv2.GaussianBlur(img,(5,5),0)
print blur