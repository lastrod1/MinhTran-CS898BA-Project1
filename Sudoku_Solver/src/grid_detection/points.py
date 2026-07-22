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

def make_grid(horizontal_lines, vertical_lines):
    if(len(horizontal_lines) != 10):
        start = horizontal_lines[0].y1
        end = horizontal_lines[-1].y1
        dist = end - start
        delta = int(dist / 9)

        new_horizontal = []
        for i in range(10):
            dist_down = i * delta
            new_line = Line(0, dist_down, 1, dist_down)
            new_horizontal.append(new_line)
    else:
        new_horizontal = horizontal_lines

    if(len(vertical_lines) != 10):
        start = vertical_lines[0].x1
        end = vertical_lines[-1].x1
        dist = end - start
        delta = int(dist / 9)

        new_vertical = []
        for i in range(10):
            dist_across = i * delta
            new_line = Line(dist_across, 0, dist_across, 1)
            new_vertical.append(new_line)
    else:
        new_vertical = vertical_lines

    return new_horizontal, new_vertical

def find_points(image, lines):
    horizontal_lines, vertical_lines = get_lines(lines)
    horizontal_lines.sort(key=lambda line: line.y1)
    vertical_lines.sort(key=lambda line: line.x1)

    if(len(horizontal_lines) != 10 or len(vertical_lines) != 10):
        horizontal_lines, vertical_lines = make_grid(horizontal_lines, vertical_lines)

    point_image = image.copy()
    points = []
    for horizontal_line in horizontal_lines:
        for vertical_line in vertical_lines:
            point = get_intersection(horizontal_line, vertical_line)
            points.append(point)
            cv.circle(point_image, point, radius=5, color=(0, 0, 255), thickness=-1) 

    print(f"Horizontal count: {len(horizontal_lines)}")
    print(f"Vertical count: {len(vertical_lines)}")    
    
    return point_image, points