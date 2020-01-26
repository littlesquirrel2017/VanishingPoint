###############################################################################
# File          : main.py
# Created by    : Rahul Kedia
# Created on    : 26/01/2020
# Project       : VanishingPoint
# Description   : This file contains the main source code for the project.
################################################################################

import cv2
import numpy as np
import os
import src.macros as M


################################################################################
# Function      : FilterLines
# Parameters    : 
# Description   :
# Return        : -
################################################################################
def FilterLines(Lines, FinalLines, Image, MaxLinesRequired, MinDiffForValidLine):
    CountLines = 0

    if Lines is not None:
        for Line in Lines:
            for x1, y1, x2, y2 in Line:
                X = abs(x2 - x1)
                Y = abs(y2 - y1)
                if X >= MinDiffForValidLine and Y >= MinDiffForValidLine:
                    CountLines += 1
                    cv2.line(Image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    LineArray = np.array([[x1, y1, x2, y2]])
                    FinalLines = np.append(FinalLines, LineArray, axis=0)

            if CountLines >= MaxLinesRequired:
                break

    if CountLines < MaxLinesRequired:
        if MaxLinesRequired < M.MIN_NUM_OF_LINES_FOUND:
            if MinDiffForValidLine > 2:
                FilterLines(Lines, FinalLines, Image, M.MAX_NUM_OF_LINES_REQUIRED, MinDiffForValidLine - 1)
            else:
                print("Not enough ines found for estimating vanishing point."
                      "Vanishing Point in this case is estimated with whatsoever "
                      "lines are fond and cannot be accurate.")
                return FinalLines
        else:
            FilterLines(Lines, FinalLines, Image, MaxLinesRequired - 1, MinDiffForValidLine)

    cv2.imshow("Lines", Image)
    return FinalLines


################################################################################
# Function      : FindLines
# Parameter     : Image - Holds Input image for processing.
#                 GrayImage - Holds the grayscale image of Image.
#                 BlurGrayImage - Holds blur image of GrayImage.
#                 EdgeImage - Holds the image with edges found by canny edge
#                             detection.
#                 Lines - Holds coordinates of both the ends of each line
#                         found by hough lines algo.
# Description   : This function takes in the input image and coverts it to
#                 suitable form to get all the lines in the image detected
#                 by HoughLinesP algo and then returns this 2D array of lines.
# Return        : Lines
################################################################################
def FindLines(Image):
    # Converting to grayscale
    GrayImage = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    # Blurring image to reduce noise.
    BlurGrayImage = cv2.GaussianBlur(GrayImage, (3, 3), 1)
    # Applying canny edge detection
    EdgeImage = cv2.Canny(BlurGrayImage, 20, 50, apertureSize=3)

    # Finding Lines in the image
    Lines = cv2.HoughLinesP(EdgeImage, 1, np.pi / 180, 100)

    return Lines


################################################################################
# Function      : ProcessImage
# Parameter     :
# Description   : Image - Holds Input image for processing.
# Return        : -
################################################################################
def ProcessImage(Image):
    Lines = FindLines(Image)
    FinalLines = np.zeros((1, 4), dtype=int)
    FinalLines = FilterLines(Lines, FinalLines, Image.copy(), M.MAX_NUM_OF_LINES_REQUIRED, M.MIN_DIFF_FOR_VALID_LINE)
    FinalLines = np.delete(FinalLines, 0, axis=0)
    print(FinalLines)

################################################################################
# Function      : ReadInputAndProcess
# Parameters    : InputImagesFolderPath - This contains the path of
#                                         InputImages folder
#                 ImageName - Name of image to be read
#                 InputImage - Input image to be processed
#                 KeyPressed - read the key pressed by the user
# Description   : This function reads all images present in InputImages folder
#                 one by one and passes them for processing and breaks the
#                 process when spacebar is pressed.
# Return        : -
################################################################################
def ReadInputAndProcess():
    InputImagesFolderPath = os.path.abspath(os.path.join('InputImages'))

    # Read input images one by one and passing for execution
    for ImageName in os.listdir(InputImagesFolderPath):
        InputImage = cv2.imread(InputImagesFolderPath + '/' + ImageName)
        cv2.imshow(ImageName, InputImage)

        ProcessImage(InputImage)

        # Check waitkey value.
        KeyPressed = cv2.waitKey(M.WAITKEY_VALUE)
        if KeyPressed == 32:      # Break when "Spacebar" is pressed
            break
        cv2.destroyAllWindows()

    cv2.destroyAllWindows()


ReadInputAndProcess()
