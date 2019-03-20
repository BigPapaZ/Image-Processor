# Image-Processor
python3


smoothimage.py
This program consists of two functions: main() and smoothimage(). smoothimage() takes
an input image “FileImage” which is passed onto it by the main() function which takes it as a
command line parameter.

This program smoothes a given input image. The main makes an empty window, whose
width is equal to double the width of the image. It then draws out the old image into the left half
of the window. Then it calls the smoothimage(FileImage) function and stores the output image
into a variable named ‘smooth’. It sets the position of smooth at half the width of the window.
Then smooth is drawn into the window. smoothimage() smoothes the image by the following
method: An empty image of the same dimensions as the FileImage is made. Then the image is
iterated for pixel by pixel. For a given pixel-not located at the boundary- the RGB levels of the
pixels surrounding it and its own are summed up, and then integer divided by 9. This RGB value
is stored in a pixel object which allocates it to the specific pixel at the empty image later on.

To run this program: smoothimage.py <image_file_name.gif>

zoomandenhance.py
This program consists of three functions: main(), sharpenImage(), restrict(), and zoom(). main()
takes an image file as a command line parameter.

The purpose of this program is to present the image in a user interface which allows the user to
choose a specific rectangular section out of it. Then the program asks for a scaling factor as per which
the size of the image is to be increased. All of this is handled by the main() function. main() also calls 2
other functions: sharpenImage() and zoom(). The input to sharpenImage() is a copy of the input image. It
enhances the contrast of that by the following method: It iterates through the image pixel by pixel. For
each pixel not on a boundary it multiplies its RGB by 9 and subtracts the sum of the RGB of the
surrounding pixels from it. The RGB value is then used as an input for restrict function along with 0 and
225. If it is below zero, that function returns RGB At zero. If it is above 225, that function returns RGB at
225. Otherwise RGB stays constant. This RGB is assigned to a relevant pixel in a new image. This image is
then returned to the main which then uses it as am input for the zoom() function. zoom() also takes the
coordinates of the rectangular section at the image to be cut out along with the number of times the
image needs to be magnified. It creates an empty image whose area dimensions is equal to the scaling
factor into the dimensions of the input image. Then it iterates through the input image pixel by pixel and
magnifies it into the new image by putting each specific pixel from the old image into the squared the
scaling factor number of times. This new image is then returned back to the main which draws it out
into a window.

To run this program: zoomandenhance.py <image_file_name.gif>
