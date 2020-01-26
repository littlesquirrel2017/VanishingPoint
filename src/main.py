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



def FilterLines(Lines, Image):
    if Lines is not None:
        for Line in Lines:
            for x1, y1, x2, y2 in Line:
                '''TanTheta = (y2 - y1)/(x2 - x1)
                print(TanTheta)
                print("{} {} {} {}".format(x1, y1, x2, y2))
                print()'''
                if x1 != x2:
                    # Draw line.
                    cv2.line(Image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow("Lines", Image)

################################################################################
# Function      : FindLines
# Parameter     :
# Description   : Image - Holds Input image for processing.
# Return        : -
################################################################################
def FindLines(Image):
    ImageCopy = Image.copy()
    GrayImage = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    BlurGrayImage = cv2.GaussianBlur(GrayImage, (3, 3), 1)
    EdgeImage = cv2.Canny(BlurGrayImage, 20, 50, apertureSize=3)

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
    FilterLines(Lines, Image.copy())


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
