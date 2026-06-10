# README for HW1

## Setup

- setup venv with requirements from the main readme in the base directory

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
