###############################################################################
# File          : macros.py
# Created by    : Rahul Kedia
# Created on    : 26/01/2020
# Project       : VanishingPoint
# Description   : This file contains the modifiable macros (variables)
#                 used in the main source code. By playing with these
#                 variables only, one can modify the main source code
#                 to adapt to different types of OMR Sheets and we can
#                 also enhance the output of the code.
################################################################################


# WaitKey Value
WAITKEY_VALUE = 0


# Max number of lines required for determining vanishing point
MAX_NUM_OF_LINES_REQUIRED = 30
MIN_NUM_OF_LINES_FOUND = 5

# Minimum difference ((x2 - x1) & (y2 - y1)) for considering a line to be valid
MIN_DIFF_FOR_VALID_LINE = 7