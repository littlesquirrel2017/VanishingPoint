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

        #ProcessImage(InputImage)

        # Check waitkey value.
        KeyPressed = cv2.waitKey(M.WAITKEY_VALUE)
        if KeyPressed == 32:      # Break when "Spacebar" is pressed
            break

    cv2.destroyAllWindows()


ReadInputAndProcess()
