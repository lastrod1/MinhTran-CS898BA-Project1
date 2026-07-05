import numpy as np
import cv2 as cv

def isolate_digit(cell, min_area=15):
    kernel = np.ones((2, 2), np.uint8)
    opened = cv.morphologyEx(cell, cv.MORPH_OPEN, kernel)

    num_labels, labels, stats, _ = cv.connectedComponentsWithStats(opened, connectivity=8)
    h, w = cell.shape

    best_label, best_area = None, -1
    for label in range(1, num_labels):
        x, y, bw, bh, area = stats[label]
        touches_border = x == 0 or y == 0 or (x + bw) >= w or (y + bh) >= h
        if touches_border or area < min_area:
            continue
        if area > best_area:
            best_area = area
            best_label = label

    cleaned = np.zeros_like(cell)
    if best_label is not None:
        cleaned[labels == best_label] = 255
    return cleaned

def find_cells(image, points, directory):
    cells = []
    
    for i in range(1,10):
        for j in range(1,10):
            index = i * 10 + j
            point1 = points[index]
            point2 = points[index - 11]
            
            x_start, x_end, y_start, y_end = point2[0], point1[0], point2[1], point1[1]
            cell = image[y_start:y_end, x_start:x_end]
            cell = isolate_digit(cell)
            cv.imwrite(f"{directory}cell({i},{j}).png", cell)
            cells.append(cell)

    return cells

