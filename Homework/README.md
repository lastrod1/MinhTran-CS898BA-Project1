# README for HW1

## Setup

- setup venv with requirements from the main readme in the base directory
- make directory for Part2_Pictues and Part3_pictures

## Code Explanation

### Part 2

1. start by reading the img with ```img = cv.imread("./Pictures/HW1_IMG_CS898BA.png")```

2. then I printed the shape of the img variable which gave ```(1536, 2816, 3)```
   1. did the shape because openCV stores images as a numpy array
   2. the 3 represents the channels which in this case is BGR (Blue Green Red)
3. For Part 2.1, I just loopover each of the 3 channels
   1. To get stats I use built in functions from numpy and scipy and then just print out each all the stats
4. For Part 2.2, I use ```cvtColor()``` which takes in the image and a flag like COLOR_BGR2GRAY or THRESH_BINARY to do color conversions
5. Then after each conversion ```cv.imwrite()``` is used to save each image in the pictures folder
6. 2.3, 2.4
   1. ```h, s, v = cv.split(hsv)``` splits the hsv image from the previous step into its individual channels
   2. ```v = cv.equalizeHist(v)``` does histogram equalization on the v channel
   3. ```hsv = cv.merge([h,s,v])``` merges the channels back together
   4. ```normalized = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)``` changes the image back to RGB
   5. ```cv.imwrite('./Pictures/Normalized_hsv_image.png', normalized)``` saves the image
7. 2.6
   1. First a list is made of all the current images and then the rows and cols are retrieved by getting the shape of the original image. A allImages list is also made which will hold all 21 images for 2.8
   2. Then the list is looped over with a rotation happening on each image then a translation. 
   3. Then each image is saved
8. 2.8
   1. A list of the sigma values is made
   2. Then I loop over all the images and for apply a gaussian blur for each sigma level

### Part 3 Explanations

1. Started off by getting my subset of 42 images from part 2 by parsing the directorys for files ending in .png
2. Then I looped over the 42 images and did the following
   1. defined the prewitt matrices as defined in the slides
   2. took out the .png from the filename which was done by `_file_name = file_name[:-4]`
   3. if it had blurred at the beginning then I removed the first 15 characters so that I could get rid of the "blurred_images/" string
   4. loaded the image with cv.imread
   5. turned the image into grayscale
   6. did all edge detection techniques 
   7. saved all images then appended images to the list I had made earlier to store them so they're easy to plot
   8. I then create the plot for step 3.8 using a grid. (NOTE: I didn't include the transformation information when I did the affine transformations so that information is missing and just says affine true since my naming convention was poor. Also missing information from when I did the original color space changes)

#### 3.5 discussion

##### Pros and cons:

Sobel: 
Pros - unlike Prewitt it has weights on the center rows and columns of the kernel which makes it better than prewitt when it comes to noisy images
Cons - requires more computation cost due to the weights than prewitt, since it has weights it also has a chance to miss very subtle edges

Laplacian:
Pros - omnidirectional edge detection instead of just vertical or horizontal
Cons - sensitive to noise and grainy images like the base image

Canny:
Pros - good noise sepression and good for getting the shape of an image
Cons - had to hardcode the thresholds and since the images were all over the place being bright and dark there was no real good threshold to capture everything

Prewitt:
Pros - works well with images that aren't very noisy
Cons - unweighted kernels since everything is 1s or 0s which means its more sensitive to noise which is seen in how some of the images are getting the grass as an edge

**The best techniques**: From looking at the images, sobel and prewitt seemed to give the best results overall and most consistent results. 

#### 6 random Plots

I just typed in plot and held down the down arrow and randomly stopped

![1st random](./Part3_Pictures/blurred1_sigma3.5_plot.png)
![2nd random](./Part3_Pictures/blurred12_sigma3.0_affine_plot.png)
![3rd random](./Part3_Pictures/affine8_plot.png)
![4th random](./Part3_Pictures/blurred15_sigma0.5_affine_plot.png)
![5th random](./Part3_Pictures/affine14_plot.png)
![6th random](./Part3_Pictures/blurred20_sigma2.0_affine_plot.png)

# Part for HW2

### Part 2

```
# Part 2

import cv2 as cv
import numpy as np
from pathlib import Path

#BGR
img = cv.imread("./Part2_Pictures/HW1_IMG_CS898BA.png")

b = img[:, :, 0]
g = img[:, :, 1]
r = img[:, :, 2]

b = cv.equalizeHist(b)
g = cv.equalizeHist(g)
r = cv.equalizeHist(r)
equalized_img = cv.merge([b, g, r])
```

- All this code does is import the necessary libraries then load the image. Since the img comes in as a numpy array I split it by slicing it. Then I apply Histogram Equalization on each channel individually by calling the function then I merge the channels together

### Part 3

```
# Part 3

grayscale = cv.cvtColor(normalized_img, cv.COLOR_BGR2GRAY)

ret, otsu = cv.threshold(grayscale, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
show_image(otsu, "Otsu's Global Thresholding")

gauss = cv.adaptiveThreshold(grayscale, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 31, 5)
show_image(gauss, "Adaptive Thresholding")

cv.imwrite("./Hw2_Pictures/OtsuGlobalThresholding.png", otsu)
cv.imwrite("./Hw2_Pictures/AdaptiveThresholding.png", gauss)

otsu_fg = cv.bitwise_and(normalized_img, normalized_img, mask=otsu)
gauss_fg = cv.bitwise_and(normalized_img, normalized_img, mask=gauss)
cv.imwrite("./Hw2_Pictures/OtsuForeground.png", otsu_fg)
cv.imwrite("./Hw2_Pictures/AdaptiveForeground.png", gauss_fg)
```

- The normalized image from the previous part is grayscaled then otsu.
  - otsu params:
    - grayscale image
    - placeholder thresholder since otsu ignores it
    - 255 value given to mixels if they meet the thresh hold value
    - THRESH_BINARY_INV was used here instead of THRESH_BINARY due to the image being dark and THRESH_OTSU was used to tell openCV to use OTSU's algorithm
- The image is then shown and then adaptive threshing holding is done on the grayscaled image
  - adaptive thresholding params:
    - grayscale image is the image we're working on
    - 255 is the max value and is same as otsu
    - ADAPTIVE_THRESH_GAUSSIAN_C is the method
    - THRESH_BINARY_INV is the same as otsu
    - 31 is the block size that the algorithm looks at. So its looking at a 31x31 block for every pixel
    - 5 is the amount that is subtracted after math is done
- foregrounds of each image is then extracted with the AND and then foregrounds are saved

### Part 4
```
# Part 4

hsv_normalized = cv.cvtColor(normalized_img, cv.COLOR_BGR2HSV)

pixel_vals = hsv_normalized.reshape((-1,3))
pixel_vals = np.float32(pixel_vals)

# 100 iterations, 85% acc
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.85)
k = 5
retval, labels, centers = cv.kmeans(pixel_vals, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

centers = np.uint8(centers)
segmented_data = centers[labels.flatten()]

segmented_image = segmented_data.reshape((hsv_normalized.shape))

show_image(segmented_image, "segmented image")
cluster_num = 4

mask = np.uint8(labels.flatten() == cluster_num) * 255
mask = mask.reshape(hsv_normalized.shape[:2])

foreground = cv.bitwise_and(normalized_img, normalized_img, mask=mask)

show_image(foreground, "Isolated Cluster")
show_image(mask, "Mask")

cv.imwrite("./Hw2_Pictures/Kmeans_foreground.png", foreground)
cv.imwrite("./Hw2_Pictures/Kmeans_mask.png", mask)
```

1. first the imaged is turned into the HSV color space and normalzied. Then since opencv required float32 for k-means the pixels values are all turned to float32
2. the criteria for my kmeans is that if 100 iterations happens or if the custers move by less than 85%. k = 5 is for 5 clusters
3. k means is then ran and everthing is passed, the 10 variable means that it'll run 10 times and return the best result
4. centers are then separated and I picked the 5th cluster since I ran checked all the clusters and the last cluster gave the correct 4 ground.
5. The mask is then turned into a binary mask and teh foreground is extract with the same method as with otsu and adapative thresholding
6. images are then shown and saved

### Part 5

```
# Part 5

mask_gt = cv.imread("./Hw2_Pictures/MASK.png")
mask_gt = cv.cvtColor(mask_gt, cv.COLOR_BGR2GRAY)
_, mask_gt = cv.threshold(mask_gt, 0, 255, cv.THRESH_BINARY)
show_image(mask_gt, "mask")
cv.imwrite("./Hw2_Pictures/ground_truth.png", mask_gt)

# Part 5.2 

def metrics(mask, gt):
    mask = mask.astype(bool)
    gt = gt.astype(bool)
    intersect = np.logical_and(mask, gt)
    union = np.logical_or(mask, gt)
    mag_int = intersect.sum()
    mag_union = union.sum()
    iou = mag_int / mag_union
    
    # dice 
    dice = (2 * mag_int) / (mask.sum() + gt.sum())
    return iou, dice

masks = [otsu, gauss, mask]

iou, dice = metrics(masks[0], mask_gt)
print(f"Otsu: IoU = {iou:.4f}, Dice = {dice:.4f}")

iou, dice = metrics(masks[1], mask_gt)
print(f"gauss: IoU = {iou:.4f}, Dice = {dice:.4f}")

iou, dice = metrics(masks[2], mask_gt)
print(f"K-Means: IoU = {iou:.4f}, Dice = {dice:.4f}")
```

1. the mask of the figure is brought in and and turned into a binary mask and saved as the ground truth. The mask I made doesn't have a background so all pixels were just turned white
2. I then define a metrics function which computes the iou and dice coeffcient 

![comparison plots](./Hw2_Pictures/comparison_plot.png)

#### 5.1 Qualitative analysis

*Discuss the pros and cons of each approach regarding background noise (e.g., leaves, porch structures) and edge preservation of the central figure. Specifically note how color normalization across all three channels impacted the final segmentation compared to the raw image results from Homework One.*

**Otsu**: otsu did well at capturing the shape of the figure however it captured the grass, porches, and trees as well which caused its scores to be low. 

**Adaptive**: Captured the edges of the main figure very well however it also captured the edges everything which is a major con since we just wanted the main figure

**K means**: This worked very well due to the HSV conversion which gave color groups which separated the main image well. The problem was that the HSV also bunched up some of the background like the trees and houses which caused its score to go down. But out of the 3, it had the highest scores

**Normalization** helped the final result quite a bit since without it the image would be too dark so everything like the grass, porches, and trees might all blend in together when doing segmentation which is what we saw on Homework one.
