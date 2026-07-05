import cv2 as cv
import numpy as np
from preprocessing import preprocessing
from probabilistic_hough import probabilistic_hough, draw_lines
from points import find_points
from cells import find_cells

# Testing of image processinging
RAW_IMAGE_DIR = "../../images/raw_images/"
TEST_IMAGE_DIR = "../../images/test_images/"
CELLS_DIR = "../../images/cells_images/"
RAW_IMAGE_FILE = "raw_1.png"
IMAGE = RAW_IMAGE_DIR + RAW_IMAGE_FILE

image = cv.imread(IMAGE)
preprocessed = preprocessing(image)
cv.imwrite(f"{TEST_IMAGE_DIR}preprocessing.png", preprocessed)

lines_image, lines = probabilistic_hough(preprocessed)
lines_image = draw_lines(image, lines)
cv.imwrite(f"{TEST_IMAGE_DIR}lines_image.png", lines_image)

points_image, points = find_points(lines_image, lines)
cv.imwrite(f"{TEST_IMAGE_DIR}points_image.png", points_image)

find_cells(preprocessed, points, CELLS_DIR)