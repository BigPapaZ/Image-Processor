#######################
# zoomandenhance.py.py
# Zaigham
# Zooms into a given image's specfic section by a given factor and increases its contrast
#######################


import cImage
import sys

def zoom(image, upperLeftX, upperLeftY, lowerRightX, lowerRightY, scalingFactor):

    '''
    This object takes in an image and the coordinates of a specific rectangular section with in that image, cuts out
    that section and increases its size.
    Input: The image with the coordinates of the corners of a rectangular section to be cut out along with the number of
    times the size of the image needs to be increased.
    Output: The cut zoomed-out section
    '''


    #creating an empty image template where the new output image will be put at
    newImg = cImage.EmptyImage((lowerRightX-upperLeftX+1) * scalingFactor,(1+lowerRightY-upperLeftY) * scalingFactor)

    #iterating through the entire image pixel by pixel
    for x_coordinate in range(upperLeftX, lowerRightX+1):      #a specific column
        for y_coordinate in range(upperLeftY, lowerRightY+1):  #a specific pixel by row in a column
            p=image.getPixel(x_coordinate, y_coordinate)

            #making an enlarged template for the to-be-edited image
            newX=(x_coordinate-upperLeftX)*scalingFactor
            newY=(y_coordinate-upperLeftY)*scalingFactor

            for i in range(scalingFactor):
                for j in range(scalingFactor):
                    newImg.setPixel(newX+i,newY+j,p) #giving each specific pixel in the its relevant RGB
                                                     #characterisitics
    return newImg


def restrict(num, minNum, maxNum):
    '''Gets three inputs and uses comparison operators to determine where one of the imputs, 'num' lies with respect to
    the others, 'maxNum' and 'minNum'. Then it returns acccordingly
    Input: num, minNum, maxNum
    Output: Returns one of the inputs, depending on the previously mentioned conditions.'''
    if num<=maxNum and num>=minNum: return num
    elif num>maxNum: return maxNum
    else: return minNum

def sharpenImage(image):
    '''
    This object increases the sharpness of an image by nultiplying a given pixel's RGB intensities by 9 and then
    subtracting the neighbouring pixel's RGB from it. The resulting RGB is put up into the relevant pixel foe the new
    image.
    InputL the image to be sharpened
    Output: the sharpened image
    '''
    cols = image.getWidth()
    rows = image.getHeight()

    newImg = cImage.EmptyImage(cols, rows)

    Red = 0
    Green = 0
    Blue = 0


    #iterating through the entire image pixel by pixel
    for x in range(cols):         #a specific column
        print(str(round(x / cols * 100, 1)) + "%")
        for y in range(rows):     #a specific pixel by row in that column
            try:
                #iterating for all the pixel surrounding a given pixel, including that pixel itself
                for x_factor in range(-1, 2):
                    for y_factor in range(-1, 2):
                        p = image.getPixel(x + x_factor, y + y_factor)     #defining a pixel object

                        Red += p.getRed()
                        Green += p.getGreen()
                        Blue += p.getBlue()

                q =image.getPixel(x, y)              #defining a pixel object which will contain the edited RGB levels


                Red_req = q.getRed() * 10-Red      #It was multiplied by 10 itstead of a 9 because the colour that is
                                                   #being subtracted, named 'Red' here, contains the central pixels color
                                                   #intensity as well. Instructions specifically ruled out subtracting
                                                   #a specific pixel's colour intensity from itself.


                # the resulting RGB might be greater or less than zero.
                Red_req=restrict(Red_req, 0, 225)


                Green_req = q.getGreen()*10-Green
                Green_req_req = restrict(Green_req, 0, 225)

                Blue_req = q.getBlue()*10-Blue
                Blue_req = restrict(Blue_req, 0, 225)

                Red = 0                       #Recalibration of the RGB back to 0 needs to be done after every iteration
                Green = 0
                Blue = 0

                q = image.getPixel(x, y)          #Defining a new pixel object

                q.setRed(Red_req)                 #Putting up the new shaprend RGB levels into the pixels
                q.setGreen(Green_req)
                q.setBlue(Blue_req)

                newImg.setPixel(x, y, q)
            except:
                p = image.getPixel(x, y)          #This is done for the pixels at the borders.
                                                  #They dont have 8 neighbours. It lets them retain their old RGB leevls.
                newImg.setPixel(x, y, p)
    return newImg


def main():
    """Takes an image filename as a command line argument. The function allows the user to select a region to zoom in on
    using the mouse as well as to specify a scaling factor. The region is "Zoomed...and Enhanced!" and displayed on the
    screen."""
    filename = sys.argv[1]

    #Create two copies of the given image
    #One that we will draw a green box on
    image = cImage.FileImage(filename)
    #The other we will pass to the processing functions
    imageCopy = cImage.FileImage(filename)

    #Display the given image
    originalWin = cImage.ImageWin("Original", image.getWidth(), image.getHeight())
    image.draw(originalWin)

    #Keeps asking the user to pick a region to zoom in on
    #until they make a valid choice
    picked = False
    while not picked:
        print("Please click the upper-left corner of the region")
        upperLeft = originalWin.getMouse()
        print("Please click the lower-right corner of the region")
        lowerRight = originalWin.getMouse()
        
        if lowerRight[0] < upperLeft[0] or lowerRight[1] < upperLeft[1]:
            print("Not a valid region")
        else:
            picked = True

    #Have to adjust the coordinates in the windw to account 
    #for the white border created by cImage
    ulX = upperLeft[0] - 5
    ulY = upperLeft[1] - 5
    lrX = lowerRight[0] - 5
    lrY = lowerRight[1] - 5

    #Create a green pixel for drawing a box around the zoom region.
    boxPixel = cImage.Pixel(0, 255, 0)

    #Draw the top and bottom sides of the box
    for x in range(ulX, lrX + 1):
        if ulY > 0:
            image.setPixel(x, ulY - 1, boxPixel)
            
        if lrY < image.getHeight() - 1:
            image.setPixel(x, lrY + 1, boxPixel)

    #Draw the left and right sides of the box
    for y in range(ulY, lrY + 1):
        if ulX > 0:
            image.setPixel(ulX - 1, y, boxPixel)

        if lrX < image.getWidth() - 1:
            image.setPixel(lrX + 1, y, boxPixel)

    #Keeps asking the user for a scaling factor
    #until they input something that is at least 1.
    scale = 0
    while scale <= 0:
        scale = int(input("Please pick a scaling factor (at least 1): "))

    print("Zooming and Enhancing...")
    
    #Sharpen the image ("enhance")
    enhanced = sharpenImage(imageCopy)
   
    #Zoom in on the specified region
    zoomed = zoom(enhanced, ulX, ulY, lrX, lrY, scale)

    #Display the enhanced and zoomed image
    zoomWin = cImage.ImageWin("Zoom...and Enhance!", zoomed.getWidth(), zoomed.getHeight())
    zoomed.draw(zoomWin)

    print("Click the zoom window to exit, when ready.")
    zoomWin.exitOnClick()

main()