import cv2 as cv
import numpy as np
from line import Line

def get_lines(lines):
    horizontal_lines = []
    vertical_lines = []

    for line_ in lines:
        x1, y1, x2, y2 = line_[0]
        new_line = Line(x1, y1, x2, y2)

        if new_line.direction == "vertical":
            is_duplicate = False
            for vert_line in vertical_lines:
                pixels_tol = 30
                if abs(vert_line.x1 - new_line.x1) <= pixels_tol:
                    is_duplicate = True
                    break
            if not is_duplicate:
                vertical_lines.append(new_line)
        else:
            is_duplicate = False
            for hor_line in horizontal_lines:
                pixels_tol = 30
                if abs(hor_line.y1 - new_line.y1) <= pixels_tol:
                    is_duplicate = True
                    break
            if not is_duplicate:
                horizontal_lines.append(new_line)

    return horizontal_lines, vertical_lines

def get_intersection(line1, line2):
    m1, m2 = line1.m, line2.m

    # y=mx+b just finding b here
    # rearrange to get y - mx = b
    b1 = line1.y1 - m1 * line1.x1
    b2 = line2.y1 - m2 * line2.x1

    # set ys to be equal so mx + b = mx + b
    # solving for x so mx - mx = b - b
    # then divide m over 
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return (int(x), int(y))

def find_points(image, lines):
    horizontal_lines, vertical_lines = get_lines(lines)

    points = []
    for horizontal_line in horizontal_lines:
        for vertical_line in vertical_lines:
            point = get_intersection(horizontal_line, vertical_line)
            points.append(point)
            cv.circle(image, point, radius=5, color=(0, 0, 255), thickness=-1) 
    
    return image, points