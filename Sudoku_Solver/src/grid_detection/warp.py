import cv2 as cv
import numpy as np
from preprocessing import preprocessing


def order_points(pts):
    pts = pts.reshape(4, 2).astype("float32")

    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)

    top_left = pts[np.argmin(s)]
    bottom_right = pts[np.argmax(s)]
    top_right = pts[np.argmin(diff)]
    bottom_left = pts[np.argmax(diff)]

    return np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32")


def find_puzzle_contour(binary):
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    h, w = binary.shape
    image_area = h * w

    candidates = []

    for contour in contours:
        area = cv.contourArea(contour)
        if area < image_area * 0.15:
            continue

        peri = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, 0.03 * peri, True)

        if len(approx) != 4:
            continue

        x, y, bw, bh = cv.boundingRect(approx)
        aspect = bw / float(bh)

        if 0.6 <= aspect <= 1.4:
            candidates.append((area, approx))

    if not candidates:
        return None

    return max(candidates, key=lambda item: item[0])[1]


def warp_puzzle(image, size=450):
    preprocessed = preprocessing(image)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    closed = cv.morphologyEx(preprocessed, cv.MORPH_CLOSE, kernel, iterations=2)

    contour = find_puzzle_contour(closed)

    if contour is None:
        raise ValueError("Could not find Sudoku puzzle contour")

    src = order_points(contour)
    dst = np.array(
        [
            [0, 0],
            [size - 1, 0],
            [size - 1, size - 1],
            [0, size - 1],
        ],
        dtype="float32",
    )

    matrix = cv.getPerspectiveTransform(src, dst)
    warped = cv.warpPerspective(image, matrix, (size, size))

    return warped, matrix