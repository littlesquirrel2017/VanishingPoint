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
# Function      :
# Parameter     :
# Description   :
# Return        :
################################################################################
def DrawLine(LineCountArray, FinalLines):
    Height, Width = LineCountArray.shape
    for x1, y1, x2, y2 in FinalLines:
        theta = np.arctan(((y2 - y1)/(x2 - x1)))
        for r in range(1, 1000):
            x0 = int(round(x1 + r*np.cos(theta)))
            y0 = int(round(y1 + r*np.sin(theta)))

            if 0 <= x0 < Width and 0 <= y0 < Height:
                LineCountArray[y0, x0] = 255

        cv2.imshow("LineCountArray", LineCountArray)
        cv2.waitKey(0)


################################################################################
# Function      : DetermineVanishingPoint
# Parameter     : ImageShape - Holds the shape of the image
#                 FinalLines - Holds the details of lines selected for detection
#                              of vanishing point.
#                 LineCountArray - 2D array which will count the number of
#                                  lines present at every pixel.
# Description   :
# Return        :
################################################################################
def DetermineVanishingPoint(ImageShape, FinalLines):
    LineCountArray = np.zeros((ImageShape[0], ImageShape[1]), dtype=float)
    DrawLine(LineCountArray, FinalLines)



################################################################################
# Function      : FilterLines
# Parameters    : Image - Holds Input image for processing.
#                 Lines - Holds coordinates of both the ends of each line
#                         found by Hough lines algo.
#                 FinalLines - Holds the details of lines selected for detection
#                              of vanishing point.
#                 MaxLinesRequired - Maximum number of lines required for
#                                    determining vanishing point in a image.
#                 MinDiffForValidLine - Minimum difference between (x2 and x1)
#                       and (y2 and y1) for considering a line to be valid for
#                       detection. This parameter is introduced so that the
#                       point sized lines are not included which can iterate
#                       in any direction.
#                 CountLines - This counts the number of lines found valid.
# Description   : This function filters the lines found in a image according
#                 to certain threshold. If required it also modifies those
#                 thresholds and do a recursive call until conditions are
#                 specified. It takes care that modifying threshold also do not
#                 go under a certain threshold which cannot be compromised.
# Return        : FinalLines, Flag(0 if lines can be detected and
#                                  -1 if cannot be detected.)
################################################################################
def FilterLines(Lines, FinalLines, Image, MaxLinesRequired, MinDiffForValidLine):
    CountLines = 0
    # Check if Lines is empty or not
    if Lines is not None:
        for Line in Lines:
            for x1, y1, x2, y2 in Line:     # Coordinates of both ends of a line
                # Length(X) and Height(Y) of horizontal edge of the triangle formed by considering line as hypotenuse.
                X = abs(x2 - x1)
                Y = abs(y2 - y1)
                # Check if height and length of triangle is greater than specified threshold.
                if X >= MinDiffForValidLine and Y >= MinDiffForValidLine:
                    # Increment count of lines found.
                    CountLines += 1
                    # Drawing line. (Can be omitted)
                    cv2.line(Image, (x1, y1), (x2, y2), (0, 255, 0), 1)
                    # Append FinalLines array.
                    LineArray = np.array([[x1, y1, x2, y2]])       # Dummy array to append FinalLines
                    FinalLines = np.append(FinalLines, LineArray, axis=0)

            # Check if enough lines are found.
            if CountLines >= MaxLinesRequired:
                break

    # Not enough lines found(No line found).
    else:
        print("Not enough lines found for estimating vanishing point.")
        return FinalLines, -1

    if CountLines < MaxLinesRequired:
        if MaxLinesRequired < M.MIN_NUM_OF_LINES_FOUND:
            if MinDiffForValidLine > 2:
                FilterLines(Lines, FinalLines, Image, M.MAX_NUM_OF_LINES_REQUIRED, MinDiffForValidLine - 1)
            else:
                print("Not enough lines found for estimating vanishing point.")
                return FinalLines, -1
        else:
            FilterLines(Lines, FinalLines, Image, MaxLinesRequired - 1, MinDiffForValidLine)

    cv2.imshow("Lines", Image)
    return FinalLines, 0


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
# Parameter     : Image - Holds Input image for processing.
#                 Lines - Holds coordinates of both the ends of each line
#                         found by Hough lines algo.
#                 FinalLines - Holds the details of lines selected for detection
#                              of vanishing point.
#                 Flag - Tells that the vanishing point for the image can be
#                        found or not.
# Description   : This function takes in image for determination of vanishing
#                 point, passes it to other functions for processing and finally
#                 shows the vanishing point.
# Return        : (The process is not completed if Flag value becomes -1)
################################################################################
def ProcessImage(Image):
    # Finding all the lines in the image.
    Lines = FindLines(Image)
    # Creating variable for holding selected/filtered lines.
    FinalLines = np.zeros((1, 4), dtype=int)
    # Filtering lines for detection of vanishing point
    FinalLines, Flag = FilterLines(Lines, FinalLines, Image.copy(), M.MAX_NUM_OF_LINES_REQUIRED,\
                                   M.MIN_DIFF_FOR_VALID_LINE)
    # Deleting the default value created when initialising the array.
    FinalLines = np.delete(FinalLines, 0, axis=0)

    # Checking Flag
    if Flag == -1:
        return

    DetermineVanishingPoint(Image.shape, FinalLines)


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
