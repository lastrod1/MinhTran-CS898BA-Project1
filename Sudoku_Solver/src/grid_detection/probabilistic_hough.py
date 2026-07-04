import cv2 as cv
import numpy as np

def draw_lines(image, lines):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(image, (x1, y1), (x2, y2), (255,0,0), 3)

    return image

def probabilistic_hough(image):
    # should take in the binary image
    MINLINELENGTH = image.shape[1] // 4
    lines = cv.HoughLinesP(image, 1, np.pi/180, 68, minLineLength=MINLINELENGTH, maxLineGap=20)

    image = draw_lines(image, lines)

    return image, lines


