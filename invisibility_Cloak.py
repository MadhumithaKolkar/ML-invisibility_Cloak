import cv2
import numpy


# Initialization function for call the trackbar
def call_trackbar(x):
    # No action needed, just a reference.
    print("")


# Camera Initialization
cap = cv2.VideoCapture(1)
# Creates six bars for upper hsv and lower hsv
bars = cv2.namedWindow("bars")

# Creating the trackbar
# Max value for hue is 180, Max of value and saturation is 255
cv2.createTrackbar("upper_hue", "bars", 110, 180, call_trackbar)
cv2.createTrackbar("upper_saturation", "bars", 255, 255, call_trackbar)
cv2.createTrackbar("upper_value", "bars", 255, 255, call_trackbar)
cv2.createTrackbar("lower_hue", "bars", 68, 180, call_trackbar)
cv2.createTrackbar("lower_saturation", "bars", 55, 255, call_trackbar)
cv2.createTrackbar("lower_value", "bars", 54, 255, call_trackbar)

# Capture initial frame for the background creation
while (True):
    cv2.waitKey(1000)
    ret, init_frame = cap.read()
    # check if the frame is returned then break
    if (ret):
        break

# Start capturing all consecutive frames
while (True):
    ret, frame = cap.read()
    # BGR to HSV conversion
    inspect = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Upper and lower values for view saturation is obtained from the trackbars
    # getting the HSV values for masking the cloak
    # getTrackbarPos() - Gets the current position number of the trackbar
    upper_hue = cv2.getTrackbarPos("upper_hue", "bars")
    upper_saturation = cv2.getTrackbarPos("upper_saturation", "bars")
    upper_value = cv2.getTrackbarPos("upper_value", "bars")
    lower_value = cv2.getTrackbarPos("lower_value", "bars")
    lower_hue = cv2.getTrackbarPos("lower_hue", "bars")
    lower_saturation = cv2.getTrackbarPos("lower_saturation", "bars")

    # Kernel to be used for dilation to remove impurities from camera stream
    # numpy.ones() creates a (n,n) matrix of 1s
    kernel = numpy.ones((3, 3), numpy.uint8)

    # Create two small arrays that hold the values of lower and upper hsv
    upper_hsv = numpy.array([upper_hue, upper_saturation, upper_value])
    lower_hsv = numpy.array([lower_hue, lower_saturation, lower_value])

    # @inspect contains the frame that was converted into hsv
    # Subtract lower_hsv from upper_hsv and create a mask for that range in the middle
    mask = cv2.inRange(inspect, lower_hsv, upper_hsv)
    # Further remove impurities
    mask = cv2.medianBlur(mask, 3)
    mask_inv = 255 - mask
    mask = cv2.dilate(mask, kernel, 5)

    # The mixing of frames in a combination to achieve the required output frame
    b = frame[:, :, 0]
    g = frame[:, :, 1]
    r = frame[:, :, 2]
    # Makes the mentioned color space area of the video stream blank using bitwise_and
    b = cv2.bitwise_and(mask_inv, b)
    g = cv2.bitwise_and(mask_inv, g)
    r = cv2.bitwise_and(mask_inv, r)
    # Merges b,g and r values for a consolidated frame
    frame_inv = cv2.merge((b, g, r))

    b = init_frame[:, :, 0]
    g = init_frame[:, :, 1]
    r = init_frame[:, :, 2]
    b = cv2.bitwise_and(b, mask)
    g = cv2.bitwise_and(g, mask)
    r = cv2.bitwise_and(r, mask)
    blanket_area = cv2.merge((b, g, r))

    final = cv2.bitwise_or(frame_inv, blanket_area)

    cv2.imshow("Invisibility Cloak", final)

    if (cv2.waitKey(3) == ord('q')):
        break;

# Always call these - to deallocate usage of camera etc, to prevent cpu usage unnecessarily.
cv2.destroyAllWindows()
cap.release()