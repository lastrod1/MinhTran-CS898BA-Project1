import cv2 as cv
import numpy as np

# Grayscale -> gaussian blur-> adaptive thresholding
def preprocessing(image):
    
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gaussian = cv.GaussianBlur(gray, (5,5), 0)
    adaptive_thresholding = cv.adaptiveThreshold(gaussian, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV,
                                                 blockSize=17, 
                                                 C=2 )
    
    return adaptive_thresholding