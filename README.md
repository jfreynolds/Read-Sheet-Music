# Read-Sheet-Music

Idea I had to try and get information about sheet music using OpenCV.

Currently reads in a PNG file for a line of music and isolates the notes from the staff lines using the morphological operations erode and
dilate. Using the now isolated staff lines, it calculates the average y coordinate values for each staff line. This will be used to compare
with the notes coordinate values in order to try and guess what note it is.

## Example ##
![Starting Image](https://github.com/jfreynolds/Read-Sheet-Music/blob/master/images/src.pngi)

![Isolated Staff Lines](https://github.com/jfreynolds/Read-Sheet-Music/blob/master/images/isolatedStaffLines.png)

Although the beam connecting the ascending eighth notes is kept in the image of the isolated staff
lines, it is ignored when finding the coordinates of the lines using the Hough Lines Algorithm,
which searches for lines of a minimum length.

![Isolated Notes](https://github.com/jfreynolds/Read-Sheet-Music/blob/master/images/isolatedNotes.png)

## Ideas going forward: ##
* Use mean shift algorithm to find center of note
* Compare note coordinate with staff line coordinate to guess note
