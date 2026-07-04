import cv2 as cv
import numpy as np
from preprocessing import preprocessing

# Testing of image processinging
RAW_IMAGE_DIR = "../../images/raw_images/"
TEST_IMAGE_DIR = "../../images/test_images/"
RAW_IMAGE_FILE = "raw_1.png"
IMAGE = RAW_IMAGE_DIR + RAW_IMAGE_FILE

image = cv.imread(IMAGE)
preprocessed = preprocessing(image)
cv.imwrite(f"{TEST_IMAGE_DIR}preprocessing.png", preprocessed)