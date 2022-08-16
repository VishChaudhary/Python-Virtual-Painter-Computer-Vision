#   Virtual Painter:
#
#       Paint on your webcam using your fingers. You can select from the following colors: pink, blue,
#   red, green, orange, yellow, and an eraser. You can also choose from a thick, medium, or thin brush thickness.
#   You can select different colors and brush thickness' using two fingers. When your index and middle fingers are up
#   your in selection mode and a rectangle is placed on the tips of your index and middle fingers as a visual indicator.
#   When only the index finger is up you are in drawing mode and can draw on your live webcam feed.
#
#   Author: Vish Chaudhary
#   Github: https://github.com/VishChaudhary






import cv2
import numpy as np
import os
import HandTrackingModule as mod

folderPath = 'Virtual Painter UI 1 [Resize]' #folder path
folder_content = os.listdir(folderPath) #folder_content is a list with the name of the contents of the folder as its values
sorted_content = sorted(folder_content)
overlay_list = []   #empty list that will be used to store the overlays. The folder_content will fill the list
            #one by one using a for loop.

for imPath in sorted_content:   #for image path in folder_content
    image = cv2.imread(f'{folderPath}/{imPath}')    #imports the different images from the folder one at a time. This is
                                            #complete path that needs to be read from
    overlay_list.append(image)  #adds each of the 10 different selection images onto our list of overlays

header = overlay_list[2]    #initial header that will display when painter is ran for the first time(initial color selection)
draw_color = (196, 102, 255) #initial color that will draw.
brush_thickness = 10
eraser_thickness = 20
px, py = 0, 0 #px- previous x, py- previous y.
img_canvas = np.zeros([720, 1280, 3], dtype = np.uint8)#((720,1080,3) - height,width, channel (RGB) 3= color. np.uint8 =unsinged 8-bit int
        #so we can get color up to 255 for the rgb color codes.

cap = cv2.VideoCapture(0)   #capture video from built in camera
cap.set(3, 1280) #3- width. #sets the dimmensions to 1280x720 which is what our UI images were sized at as well.
cap.set(4, 720)  #4- height. #the 3 and 4 are referencing different properties of the image, I couldn't find out anymore than that vague explanation.

detector = mod.handDetector(detectionCon= 0.65, maxHands= 2) #hand detection confidence is increased from 0.5 to 0.85 to make
    #sure it doesn't accidentally draw something by incorrect detection. Reduces tracking error.
#infintie loop

while True:

    #1. Import image
    success, img = cap.read()  # read image into img
    img = cv2.flip(img, 1) #flips the image in the first direction (horizontal direction)

    #2. Find hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, False)
    present_hand = detector.handedness(img)

    if len(lmList)!= 0:  # will print the pixel position only if a hand is present. Checks to see if a hand is present.
        #print(lmList)  # This will print the pixel position of the specified landmark. In this case it's all of them

        #tip of index finger
        x1, y1 = lmList[8][1:]   #x1, y1 is the tip coordinates of the index finger. [8] is landmark 8 which is the index
                #finger. [1:] from element 1 till the end. Theres 3 elements but the count starts at zero so 1 referes to element 2.
        #tip of middle finger
        x2, y2 = lmList[12][1:]

        #3. Check which fingers are up
        fingers_up = detector.fingerCounter()   #detects which fingers are up and which are down


        #4. Selection mode- Two fingers up
        if fingers_up[1] and fingers_up[2] and fingers_up[3]== False and fingers_up[4]==False:
            px, py = 0, 0
            if present_hand == 'Right':
                cv2.rectangle(img, (x1-10,y1), (x2+10,y2-15), (255,113,82), cv2.FILLED ) #visual representation of selection mode

            elif present_hand == 'Left':
                cv2.rectangle(img, (x1 + 10, y1), (x2 - 10, y2 -15), (255,113,82), cv2.FILLED)  # visual representation of selection mode

            if y1 < 105: #this means if we're in the header

                #select pink
                if 0 < x1 < 112:    #if the index finger is within this range in the x-axis then change the overlay and draw color
                    draw_color = (196, 102, 255)
                    if brush_thickness == 50:
                        header = overlay_list[0]

                    if brush_thickness == 25:
                        header = overlay_list[1]

                    if brush_thickness == 10:
                        header = overlay_list[2]

                #select blue
                elif 112 < x1 < 229:
                    draw_color = (207, 36, 11)
                    if brush_thickness == 50:
                        header = overlay_list[3]

                    if brush_thickness == 25:
                        header = overlay_list[4]

                    if brush_thickness == 10:
                        header = overlay_list[5]

                #select red
                elif 229 < x1 < 351:
                    draw_color = (22, 22, 255)
                    if brush_thickness == 50:
                        header = overlay_list[6]

                    if brush_thickness == 25:
                        header = overlay_list[7]

                    if brush_thickness == 10:
                        header = overlay_list[8]

                #select green
                elif 351 < x1 < 473:
                    draw_color = (80, 180, 4)
                    if brush_thickness == 50:
                        header = overlay_list[9]

                    if brush_thickness == 25:
                        header = overlay_list[10]

                    if brush_thickness == 10:
                        header = overlay_list[11]

                #select orange
                elif 473 < x1 < 592:

                    draw_color = (73, 140, 248)
                    if brush_thickness == 50:
                        header = overlay_list[12]

                    if brush_thickness == 25:
                        header = overlay_list[13]

                    if brush_thickness == 10:
                        header = overlay_list[14]

                #select yellow
                elif 592 < x1 < 712:

                    draw_color = (82, 227, 255)
                    if brush_thickness == 50:
                        header = overlay_list[15]

                    if brush_thickness == 25:
                        header = overlay_list[16]

                    if brush_thickness == 10:
                        header = overlay_list[17]

                #select eraser
                elif 722 < x1 < 858:
                    draw_color = (0, 0, 0)
                    if brush_thickness == 50:
                        header = overlay_list[18]
                    if brush_thickness == 25:
                        header = overlay_list[19]
                    if brush_thickness == 10:
                        header = overlay_list[20]

                #Selecting correct header for max brush thickness and color
                if y1 < 45 and 900 < x1 < 1065:
                    brush_thickness = 50
                    if draw_color == (196, 102, 255):
                        header = overlay_list[0]
                    if draw_color == (207, 36, 11):
                        header = overlay_list[3]
                    if draw_color == (22, 22, 255):
                        header = overlay_list[6]
                    if draw_color == (80, 180, 4):
                        header = overlay_list[9]
                    if draw_color == (73, 140, 248):
                        header = overlay_list[12]
                    if draw_color == (82, 227, 255):
                        header = overlay_list[15]
                    if draw_color == (0, 0, 0):
                        header = overlay_list[18]

                # Selecting correct header for medium brush thickness and color
                if 45 < y1 < 80 and 1005 < x1 < 1150:
                    brush_thickness = 25
                    if draw_color == (196, 102, 255):
                        header = overlay_list[1]
                    if draw_color == (207, 36, 11):
                        header = overlay_list[4]
                    if draw_color == (22, 22, 255):
                        header = overlay_list[7]
                    if draw_color == (80, 180, 4):
                        header = overlay_list[10]
                    if draw_color == (73, 140, 248):
                        header = overlay_list[13]
                    if draw_color == (82, 227, 255):
                        header = overlay_list[16]
                    if draw_color == (0, 0, 0):
                        header = overlay_list[19]

                # Selecting correct header for thinest brush thickness and color
                if 80 < y1 < 105 and 1090 < x1 < 1250:
                    brush_thickness = 10
                    if draw_color == (196, 102, 255):
                        header = overlay_list[2]
                    if draw_color == (207, 36, 11):
                        header = overlay_list[5]
                    if draw_color == (22, 22, 255):
                        header = overlay_list[8]
                    if draw_color == (80, 180, 4):
                        header = overlay_list[11]
                    if draw_color == (73, 140, 248):
                        header = overlay_list[14]
                    if draw_color == (82, 227, 255):
                        header = overlay_list[17]
                    if draw_color == (0, 0, 0):
                        header = overlay_list[20]

        #5. Drawing mode - Index fingers up
        if fingers_up[1] and fingers_up[2] == False and fingers_up[3] == False and fingers_up[4]==False:

            if px == 0 and py == 0:
                px, py = x1, y1

            cv2.circle(img, (x1, y1), brush_thickness, draw_color, cv2.FILLED)  # visual representation of drawing mode
            cv2.line(img, (px,py), (x1,y1), draw_color, int(brush_thickness * 2))    #used to draw lines on our image
            cv2.line(img_canvas, (px, py), (x1, y1), draw_color, int(brush_thickness * 2))  # used to draw lines on our canvas
            px, py = x1, y1 #update previous x and y to current x and y coordinates

    imgGray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)#convert the canva into black and white
    threshold, imgInv = cv2.threshold(imgGray, 47, 255, cv2.THRESH_BINARY_INV)#converts a gray scale image to black and white. Given a pixel value anything below to is
    #is set to 0(black) and anything above to 1(given input (255-white)). cv2.
    # For every pixel, the same threshold value is applied. If the pixel value is smaller than the threshold, it is set to 0,
    # otherwise it is set to a maximum value. The function cv.threshold is used to apply the thresholding. The first argument
    # is the source image, which should be a grayscale image. The second argument is the threshold value which is used to
    # classify the pixel values. The third argument is the maximum value which is assigned to pixel values exceeding the threshold.
    # OpenCV provides different types of thresholding which is given by the fourth parameter of the function.

    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, imgInv) #draws our drawing on the display img but in black and white instead of color
    img = cv2.bitwise_or(img, img_canvas)  # converts our black drawing into their appropriate color

    #setting the header image
    img[0:105, 0:1280] = header #the image in this region (x:0 to 1280) (y:0 to 125) is equal to the header.
                #sets the image from 0 to 125 in the y-direction and 0 to 1280 in the x direction equal to the header.

    cv2.imshow('My Webcam', img)    #show the image
    cv2.waitKey(1)  #one millisecond delay