import cv2 as cv
from tensorflow.keras.models import load_model
import numpy as np
import os
import copy

def print_grid(grid):
    for i in range(9):
        print_str = f"Row {i + 1}: "
        for j in range(9):
            print_str += f"{grid[i][j]} "
        print(print_str)


def get_grid(cells):
    model_path = os.path.join(os.path.dirname(__file__), "..", "..", "models", "mnist_cnn.keras")
    model = load_model(model_path)

    grid = []
    
    for i in range(0, 81, 9):
        row_cells = cells[i : i + 9]
        row = []
        
        for cell in row_cells:
            if cv.countNonZero(cell) < 5:
                row.append(0)
                continue

            normalized_cell = cell.astype("float32") / 255.0
            normalized_cell = normalized_cell.reshape(1, 28, 28, 1)
            
            probabilities = model.predict(normalized_cell)
            predicted_digit = np.argmax(probabilities)
            
            if predicted_digit == 0:
                row.append(0)
            else:
                row.append(predicted_digit)
                
        grid.append(row)

    return grid

def draw_sudoku_grid(grid, cell_size=60):
    size = cell_size * 9
    img = np.ones((size, size, 3), dtype=np.uint8) * 255

    for i in range(10):
        thickness = 3 if i % 3 == 0 else 1
        cv.line(img, (i * cell_size, 0), (i * cell_size, size), (0, 0, 0), thickness)
        cv.line(img, (0, i * cell_size), (size, i * cell_size), (0, 0, 0), thickness)

    font = cv.FONT_HERSHEY_SIMPLEX
    for row in range(9):
        for col in range(9):
            val = grid[row][col]
            if val == 0:
                continue

            text = str(val)
            (tw, th), _ = cv.getTextSize(text, font, 1.2, 2)
            x = col * cell_size + (cell_size - tw) // 2
            y = row * cell_size + (cell_size + th) // 2

            color = (0, 0, 0)
            cv.putText(img, text, (x, y), font, 1.2, color, 2, cv.LINE_AA)

    return img

# funcs to solve with backtracking

def isSafe(mat, row, col, num):
    
    for x in range(9):
        if mat[row][x] == num:
            return False

    for x in range(9):
        if mat[x][col] == num:
            return False

    startRow = row - (row % 3)
    startCol = col - (col % 3)

    for i in range(3):
        for j in range(3):
            if mat[i + startRow][j + startCol] == num:
                return False

    return True

def solveSudokuRec(mat, row, col):
    if row == 8 and col == 9:
        return True

    if col == 9:
        row += 1
        col = 0

    if mat[row][col] != 0:
        return solveSudokuRec(mat, row, col + 1)

    for num in range(1, 10):
        
        if isSafe(mat, row, col, num):
            mat[row][col] = num
            if solveSudokuRec(mat, row, col + 1):
                return True
            mat[row][col] = 0

    return False

def solveSudoku(mat):
    mat_copy = copy.deepcopy(mat)
    if (solveSudokuRec(mat, 0, 0)):
        return mat_copy

    return None
