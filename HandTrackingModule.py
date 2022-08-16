#   Hand Tracking Module:
#
#   Hand Detector class that includes numerous useful functions related to detecting and dealing with hands in computer
#   vision. This module can also be run on its own.
#
#   findHands - detects the hands and draws the landmarks on the image if draw is set as True.
#   handedness - detects whether the right or the left hand is presented to the camera.
#   findPosition - finds the positions of the 21 different landmarks and converts them to pixel positions.
#   fingerCounter - Counts the number of fingers currently up.
#
#   Author: Vish Chaudhary
#   Github: https://github.com/VishChaudhary




import cv2
import mediapipe as mp
import time

class handDetector:
    def __init__(self, mode=False, maxHands=2, complexity = 1, detectionCon=0.5, trackCon=0.5):
        #We're going to create an object and that object will have it's own variable any time you use a variable of the object you call it self.something
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands   #self is needed here so that on the next line the correct parameters can be passed
        #by making it self.mpHands and then self.hands you can access the object correct so that self.mode and self.maxHands and etc. can
        #be assigned properly. Without the selfs here the parameters passed in by the user wouldn't actually be able to
        #be assigned to the Hands() function from the mp library and thus not used or applied.
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon,)
        self.mpDraw = mp.solutions.drawing_utils #self is needed her so the functions below can access this information.
        self.tipIds = [4,8,12,16,20]

    def findHands(self, img, draw = True):  #img passed in as a parameter so it knows what image to work with.
        imgColor = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgColor)#self here bc hands needs it which means results also needs it

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    #handNo=0 - for one hand
    def handedness(self, img):
        self.present_hand = ''
        if self.results.multi_handedness:
            for index in self.results.multi_handedness:
                for score, label in enumerate(index.classification):
                    for first, second in enumerate(label.label):
                        if second == 'L':
                            self.present_hand = 'Left'
                        if second == 'R':
                            self.present_hand = 'Right'
        return self.present_hand

    def findPosition(self, img, draw=True):
        self.lmList = [] #landmark list
        if self.results.multi_hand_landmarks:   #if hand and thus landmarks are present then
           for myHand in self.results.multi_hand_landmarks: #myHand is equal to the landmark values(x,y,z) for one hand (my handNo)
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lmList.append([id, cx, cy]) #adds (appends) the values [id, cx, cy] in that format onto the end of
                    #the lmList list.
                    if draw:
                        if id == 4 or id == 8 or id == 12 or id == 16 or id == 20:
                            cv2.circle(img, (cx, cy), 10, (255, 110, 180), cv2.FILLED)

        return self.lmList

    def fingerCounter(self,):
        fingers = []

        # Special Thumb Case- If thumb is to the left of the middle of the thumb then its closed
        # This works only for the right hand
        if len(self.present_hand) != 0:
            if self.present_hand == 'Right':
                if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
                    fingers.append(1)  # adds 1 to the fingers list for every finger that is open
                else:
                    fingers.append(0)  # adds 0 to the fingers list for every finger that is closed.
            if self.present_hand == 'Left':
                if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                    fingers.append(1)  # adds 1 to the fingers list for every finger that is open
                else:
                    fingers.append(0)  # adds 0 to the fingers list for every finger that is closed.

        # Four fingers
        for id in range(1, 5):  # from 1 to 5 because thumb gets its own special case
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][
                2]:  # Its less than rather than open because in open cv the top of the screen has a
                # lower value than the bottom, so its backwards. lmlist has 3 values in it: 0.landmark numer (0-20) 1. x-pixel coordinate
                # 2. y-pixel coordinate. Here the 2 refers to the y coordinate. This is essentially saying if the tip
                # of the finger(tipIds[id]) is less than the middle of that finger(tipIds[id] -2 )<--- this
                # is because the middle of each finger is two landmarks below its tip.
                fingers.append(1)  # adds 1 to the fingers list for every finger that is open
            else:
                fingers.append(0)  # adds 0 to the fingers list for every finger that is closed.
        return fingers


def main():
    previous_time = 0
    current_time = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()   #creating the object and using its default parameters

    #infinte loop
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)  # flips the image in the first direction (horizontal direction)
        img = detector.findHands(img)   #findHands returns the manipulated image so img is just updated.
        lmList = detector.findPosition(img)
        present_hand = detector.handedness(img)

        if len(present_hand) != 0:
            print(present_hand)

        # if len(lmList) != 0:  #will print the pixel position only if a hand is present. Checks to see if a hand is present.
        #      print(lmList[8])  #This will print the pixel position of the specified landmark. In this case it was 8.

        #fps calculations
        current_time = time.time()
        fps = 1 / (current_time-previous_time)
        previous_time = current_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 105, 180), 3) #displays fps
        cv2.imshow("My Webcam", img) #displays image
        cv2.waitKey(1)   #1 millisecond delay


if __name__ == "__main__":
    main()
