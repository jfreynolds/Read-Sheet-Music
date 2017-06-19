import cv2
from itertools import groupby
import numpy as np
from operator import itemgetter
from statistics import median
import sys

def getStaffLineCoordinates(img):
    # Finds horizontal lines in image of extracted staff lines
    lines = cv2.HoughLinesP(img, 1, np.pi/180, 100, 100, 50)
    
    # Set that contains all y coordinates found in image
    yCoordinates = set()

    # Add y coordinates to set for all horizontal lines in image
    for line in lines:
        for x1,y1,x2,y2 in line:
            yCoordinates.add(y1)

    # Sort set in order to isolate each line
    yCoordinates = sorted(yCoordinates) 

    # List to hold range of pixel coordinates for each staff line
    avgYCoordinates = []

    # Get average y-coordinate for each staff line
    for key, group in groupby(enumerate(yCoordinates), lambda i_x: i_x[0] - i_x[1]):
        avgYCoordinates.append(list(map(itemgetter(1), group)))

    # List to hold the finalized median staff coordinate values
    staffLineCoordinates = []

    # Calculate the median coordinates for each staff
    # Using median for now, but might change to mean
    # Because outliers aren't likely on paper
    for coordinates in avgYCoordinates:
        staffLineCoordinates.append(median(coordinates))

    return staffLineCoordinates

def isolateNotesFromStaffLines(img):
    # Load image
    src = cv2.imread(img)
    
    # Sanity check that it was read correctly
    # Exits otherwise
    if src is None:
        sys.stderr.write('Error loading image!')
        sys.exit(1)

    # Transform image to grayscale if needed
    gray = None

    if src.shape[2] == 3:
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    else:
        gray = src

    # Apply adaptive threshold to get binary image 
    bw = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)

    # Initializes variables used to extract horizontal/vertical lines
    horizontal = bw.copy()
    vertical = bw.copy()

    # Size on horizontal axis used for creating horizontal structuring element
    horizontalSize = horizontal.shape[1] // 30
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(horizontalSize, 1))

    # Erode everything but the staff lines
    horizontal = cv2.erode(horizontal, horizontalStructure, (-1, -1))
    horizontal = cv2.dilate(horizontal, horizontalStructure, (-1, -1))

    # Size on vertical axis for creating vertical structuring element
    verticalSize = vertical.shape[0] // 30
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalSize))

    # Erode the staff lines leaving just the isolated notes
    vertical = cv2.erode(vertical, verticalStructure, (-1, -1))
    vertical = cv2.dilate(vertical, verticalStructure, (-1, -1))

    # Inverse isolated notes images
    vertical = cv2.bitwise_not(vertical)
    
    # Extract edges in vertical and smooth the image to make notes look cleaner
    edges = cv2.adaptiveThreshold(vertical, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, -2)
    kernel = np.ones((2, 2, 1), dtype='uint8')
    edges = cv2.dilate(edges, kernel)
    smooth = vertical.copy()
    smooth = cv2.blur(smooth, (2,2))
    # Copy smooth to vertical with mask of edges
    locs = np.where(edges != 0)
    vertical[locs[0], locs[1]] = smooth[locs[0], locs[1]]

    # Average y coordinate values of staff lines
    # First element is top, last is bottom
    staffLines = getStaffLineCoordinates(horizontal)

if __name__ == '__main__':
    isolateNotesFromStaffLines(sys.argv[1])
