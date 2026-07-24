import cv2 as cv
import numpy as np

def draw_lines(image, lines, color=(0,255,0)):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(image, (x1, y1), (x2, y2), color, 3)

    return image

def probabilistic_hough(image):
    # should take in the binary image
    MINLINELENGTH = image.shape[1] // 2
    lines = cv.HoughLinesP(image, 1, np.pi/180, 68, minLineLength=MINLINELENGTH, maxLineGap=20)

    lines_image = draw_lines(image, lines)

    return lines_image, lines


