import os
import cv2
import time
import numpy as np
import HandTrackingModule as htm

brushThickness = 15
eraserThickness = 50
    # 1. Import Image
    # 2. Find Hand Ladmarks
    # 3. Check which finmgers are up
    # 4. If Selection mode - Two fingers are up
    # 5. If Drawintg Mode - Index Finger UP

folderPath = "Header"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

header = overlayList[0]
drawColor = (255, 0, 255)

pTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4,720)

detector = htm.handDetector(detectionCon=0.85)

xp, yp =0, 0

imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # 1.
    success, img = cap.read()
    img = cv2.flip(img, 1)
    # 2.
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        #print(lmList)

        # tip of index and middle finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3.
        fingers = detector.fingersUp()
        #print(fingers)

        # 4.
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("selection Mode")
            # Checking for the click
            if y1 < 125:
                if 250< x1 <450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550< x1 <750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800< x1 <950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050< x1 <1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)



        # 5.
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp==0 and yp==0:
                xp, yp = x1, y1

            if drawColor == (0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    # Setting the Header Image
    img[0:125, 0:1280] = header
    #img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.putText(img, f'FPS: {int(fps)}', (40,70), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)
    cv2.imshow("Cam", img)
    cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)
