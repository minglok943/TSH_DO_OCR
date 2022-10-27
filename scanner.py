import cv2
import numpy as np
from imutils.perspective import four_point_transform
from DO_Processing import DO
def nothing(x):
    pass

cv2.namedWindow('tune')
cv2.createTrackbar('x', 'tune', 0, 1280, nothing)
cv2.createTrackbar('x1', 'tune', 0, 1280, nothing)
cv2.createTrackbar('y', 'tune', 0, 720, nothing)
cv2.createTrackbar('y1', 'tune', 0, 720, nothing)



cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

count = 0
scale = 0.5

d_o = DO(debugEnable=True, showQuantityCrop=True)


WIDTH, HEIGHT = 1280, 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)


def scan_detection(image):
    global document_contour

    document_contour = np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [0, HEIGHT]])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                document_contour = approx
                max_area = area

    cv2.drawContours(frame, [document_contour], -1, (0, 255, 0), 3)


while True:

    _, frame = cap.read()
    #frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)


    cv2.imshow("input", cv2.resize(frame, (640, 360)))
    cv2.moveWindow("input", 0, 0)

    """
    frame_copy = frame.copy()
    scan_detection(frame_copy)
    warped = four_point_transform(frame_copy, document_contour.reshape(4, 2))
    cv2.imshow("Warped", cv2.resize(warped, (int(0.75 * warped.shape[1]), int(0.75 * warped.shape[0]))))
    cv2.moveWindow("Warped", 0, 450)
    """

    d_o.run(frame)        

    cv2.imshow("Result", d_o.board)
    cv2.moveWindow("Result", 650, 0)
    
    
    x = cv2.getTrackbarPos('x', 'tune')
    x1 = cv2.getTrackbarPos('x1', 'tune')
    y = cv2.getTrackbarPos('y', 'tune')
    y1 = cv2.getTrackbarPos('y1', 'tune')
    cropped = frame[y:y1,x:x1]
    if cropped.shape[0] != 0 and cropped.shape[1] != 0:
        cv2.imshow("cropped", cv2.resize(cropped, (int(3.0*cropped.shape[1]), int(3.0*cropped.shape[0]))))

    pressed_key = cv2.waitKey(1) & 0xFF
    
    if pressed_key == 27:
        break

    elif pressed_key == ord('s'):
        cv2.imwrite("output/scanned_" + str(count) + ".jpg", warped)
        count += 1

        cv2.imshow("input", cv2.resize(frame, (int(scale * WIDTH), int(scale * HEIGHT))))
        cv2.waitKey(500)

    elif pressed_key == ord('n'):
        self.next()
    elif pressed_key == ord('i'):
        d_o.insertDatabase()
    elif pressed_key == ord('c'):
        test_text = pytesseract.image_to_string(cropped)
        if d_o.debugEnable == True:
            d_o.secondGnome.echo(test_text)

cv2.destroyAllWindows()
d_o.secondGnome.kill()
