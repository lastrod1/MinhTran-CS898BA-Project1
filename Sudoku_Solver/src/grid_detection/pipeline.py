import cv2 as cv
import numpy as np
from preprocessing import preprocessing
from probabilistic_hough import probabilistic_hough, draw_lines
from points import find_points
from cells import find_cells
from warp import warp_puzzle
from tensorflow.keras.models import load_model
# Testing of image processinging
RAW_IMAGE_DIR = "../../images/raw_images/"
TEST_IMAGE_DIR = "../../images/test_images/"
CELLS_DIR = "../../images/cells_images/"
RAW_IMAGE_FILE = "raw_3.png"
IMAGE = RAW_IMAGE_DIR + RAW_IMAGE_FILE

image = cv.imread(IMAGE)

warped, matrix = warp_puzzle(image)
preprocessed = preprocessing(warped)
lines_image, lines = probabilistic_hough(preprocessed)
lines_image = draw_lines(warped, lines)
points_image, points = find_points(lines_image, lines)

cv.imwrite(f"{TEST_IMAGE_DIR}warped.png", warped)
cv.imwrite(f"{TEST_IMAGE_DIR}preprocessed.png", preprocessed)
cv.imwrite(f"{TEST_IMAGE_DIR}lines_image.png", lines_image)
cv.imwrite(f"{TEST_IMAGE_DIR}points_image.png", points_image)


cells = find_cells(preprocessed, points, CELLS_DIR)

model = load_model("../../models/mnist_cnn.keras")

grid = []
for cell in cells:
    cell = cell.astype("float32") / 255.0
    cell = cell.reshape(1, 28, 28, 1)
    if cv.countNonZero(cell) < 5:
        grid.append(0)
        continue
    probabilities = model.predict(cell)
    predicted_digit = np.argmax(probabilities)
    if predicted_digit == 0:
        grid.append(10)
        continue
    grid.append(predicted_digit)

for i in range(9):
    print(f"\nRow {i}:", end="")
    for j in range(9):
        row = i * 9
        print(f" {grid[row + j]}", end="")
