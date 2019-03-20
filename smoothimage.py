#######################
# smoothimage.py
# Zaigham
# Smoothes a given input image and gives the edited image as an output
#######################


import pdb
import cImage
import sys
import math


def smoothImage(FileImage):
    '''
    This function takes an image as an input and smoothes it out and returns a new imaeg
    Input: The image to be smoothed
    Output; The smoothed out image
    '''

    cols = FileImage.getWidth()
    rows = FileImage.getHeight()

    newImg = cImage.EmptyImage(cols, rows)        #creating an image object which will be edited later on


    #RGB being set to 0
    Red=0
    Green=0
    Blue=0

    #iterating through the entire image pixel by pixel
    for x in range(cols):           #a specific column
        print(str(round(x / cols * 100, 1)) + "%")
        for y in range(rows):       #a specific pixel by row in a column
            try:
                # iterating for all the pixels surrounding a given pixel, including that pixel itself
                for x_factor in range(-1, 2):
                    for y_factor in range(-1, 2):

                        p = FileImage.getPixel(x + x_factor, y + y_factor)  #defining a pixel object

                        #adding up the RGB levels from the pixels surroundings a given pixel into that pixels RGB level
                        #itself

                        Red+=p.getRed()
                        Green+=p.getGreen()
                        Blue+=p.getBlue()


                #Integar division needs to be done, because the sum of RGBs might not be a multiple of 9.
                Red_avg=Red//9
                Green_avg=Green//9
                Blue_avg=Blue//9

                #Recalibration of the RGB back to 0 needs to be done after every iteration
                Red=0
                Green=0
                Blue=0

                q = FileImage.getPixel(x, y)       #defining a pixel object which will contain the edited RGB levels

                #Editing the latter q pixel object to new RGB levels
                q.setRed(Red_avg)
                q.setGreen(Green_avg)
                q.setBlue(Blue_avg)



                newImg.setPixel(x,y,q)

            except:
                p = FileImage.getPixel(x, y)      #This is done for the pixels at the borders. They dont have 8
                                                  #neighbours. It lets them retain their old RGB leevls.
                newImg.setPixel(x, y, p)

    return newImg




def main():
    """Takes an image filename as a command line argument. This function calls another function which is responsible for
     returning another smoothed image. It handles the rest of the intricaies concerned with printing that image into
     a window etc."""
    n = sys.argv[1]

    FileImage = cImage.FileImage(n)

    w = FileImage.getWidth()
    h = FileImage.getHeight()

    Window = cImage.ImageWin("Smooth Image:", w*2, h)   #creating a window double the width of the input image
    FileImage.draw(Window)            #drawing the original image

    Smooth = smoothImage(FileImage)
    Smooth.setPosition(x=w, y=0)       #setting up the position of the edited image on the window
    Smooth.draw(Window)                #drawing the new image into the window

    Window.exitOnClick()

main()

