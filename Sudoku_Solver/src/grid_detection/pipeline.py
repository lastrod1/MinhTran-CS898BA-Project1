import cv2 as cv
import numpy as np
import os
from preprocessing import preprocessing
from probabilistic_hough import probabilistic_hough, draw_lines
from points import find_points
from cells import find_cells
from warp import warp_puzzle
from sudoku_grid import get_grid, print_grid
from tensorflow.keras.models import load_model
# Testing of image processinging
RAW_IMAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "images/", "raw_images/")
TEST_IMAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "images/", "test_images/")
CELLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "images/", "cells_images/")
RAW_IMAGE_FILE = "raw_2.png" # default 
IMAGE = RAW_IMAGE_DIR + RAW_IMAGE_FILE

def pipeline(image_path = IMAGE):
    image = cv.imread(image_path)

    warped, matrix = warp_puzzle(image)
    cv.imwrite(f"{TEST_IMAGE_DIR}warped.png", warped)

    preprocessed = preprocessing(warped)
    cv.imwrite(f"{TEST_IMAGE_DIR}preprocessed.png", preprocessed)

    lines_image, lines = probabilistic_hough(preprocessed)
    cv.imwrite(f"{TEST_IMAGE_DIR}lines_image.png", lines_image)

    lines_image_nb = draw_lines(warped, lines, color=(0, 0, 255))
    cv.imwrite(f"{TEST_IMAGE_DIR}lines_image_nb.png", lines_image_nb)

    points_image, points = find_points(lines_image_nb, lines)
    cv.imwrite(f"{TEST_IMAGE_DIR}points_image.png", points_image)

    cells = find_cells(preprocessed, points, CELLS_DIR)

    grid = get_grid(cells)
    return grid