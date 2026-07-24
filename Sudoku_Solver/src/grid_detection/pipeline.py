import cv2 as cv
import numpy as np
from preprocessing import preprocessing
from probabilistic_hough import probabilistic_hough, draw_lines
from points import find_points
from cells import find_cells
from warp import warp_puzzle
from sudoku_grid import get_grid, print_grid
from tensorflow.keras.models import load_model
# Testing of image processinging
RAW_IMAGE_DIR = "../../images/raw_images/"
TEST_IMAGE_DIR = "../../images/test_images/"
CELLS_DIR = "../../images/cells_images/"
RAW_IMAGE_FILE = "raw_1.png"
IMAGE = RAW_IMAGE_DIR + RAW_IMAGE_FILE

image = cv.imread(IMAGE)

warped, matrix = warp_puzzle(image)
cv.imwrite(f"{TEST_IMAGE_DIR}warped.png", warped)
preprocessed = preprocessing(warped)
lines_image, lines = probabilistic_hough(preprocessed)
lines_image = draw_lines(warped, lines)
points_image, points = find_points(lines_image, lines)

print(f"# of points: {len(points)}")

cv.imwrite(f"{TEST_IMAGE_DIR}preprocessed.png", preprocessed)
cv.imwrite(f"{TEST_IMAGE_DIR}lines_image.png", lines_image)
cv.imwrite(f"{TEST_IMAGE_DIR}points_image.png", points_image)



cells = find_cells(preprocessed, points, CELLS_DIR)

grid = get_grid(cells)
print_grid(grid)