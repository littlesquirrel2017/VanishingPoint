# VanishingPoint

This project aims on finding the vanishing point in a hallway image.


### Installation

[Click here for installation procedure for this project.](https://gist.github.com/KEDIARAHUL135/c490e212966fec2751d62e193f341967)


### Approach

Lines are first found with the help of Hough Line Transform and the are sorted according to their angle with respect to horizontal and length and then a new 2D array with same size counts for every pixel how manylines are crossing that pixel. The element(corresponding to the pixel) with maximum value in 2D array is estimated to be the vanishing point. The Vanishing point is finally displayed with a red circle on the image and output images are saved in a folder. 


### Bugs

Not all images are getting a correct output. This is due to lines not intersecting perfectly at a particular point causing other pixel to attain maximum value. This bug is reduced by increasing the thickness of lines but the bug still exists.


### Folder Structure

`src` folder contains the main source code for the project and input and output images folder also.
