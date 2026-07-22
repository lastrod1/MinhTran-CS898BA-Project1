import cv2 as cv
from tensorflow.keras.models import load_model
import numpy as np

def print_grid(grid):
    for i in range(9):
        print(f"\nRow {i}:", end="")
        for j in range(9):
            row = i * 9
            print(f" {grid[row + j]}", end="")

def get_grid(cells):
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
    return grid