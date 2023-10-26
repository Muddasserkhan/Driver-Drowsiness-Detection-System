# import required libraries
# This line imports the OpenCV library, which is used for image processing and computer vision tasks.
import cv2

# read input image
img = cv2.imread('img.jpg')

# convert to grayscale of each frames.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# read the haarcascade to detect the faces in an image
face_cascade = cv2.CascadeClassifier('.\Data\haarcascade_frontalface_default.xml')

# read the haarcascade to detect the eyes in an image
eye_cascade = cv2.CascadeClassifier('.\Data\haarcascade_eye_tree_eyeglasses.xml')

# detects faces in the input image
# The 'detectMultiScale' function is used to find faces in the grayscale image. The parameters '1.3' and '4' are scale factor and minimum neighbors,
# which control the sensitivity and accuracy of the detection.
faces = face_cascade.detectMultiScale(gray, 1.3, 4)

# This line simply prints the number of faces detected in the image.
print('Number of detected faces:', len(faces))

# loop over the detected faces
# This for loop iterates over each detected face, where (x, y) represents the top-left corner coordinates of the face's bounding box, and (w, h) are the width and height of the bounding box.

for (x, y, w, h) in faces:
    # Here, two regions of interest are defined, 'roi_gray' for the grayscale face and 'roi_color' for the colored face within the bounding box.
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = img[y:y + h, x:x + w]

    # detects eyes of within the detected face area (roi)
    # The 'detectMultiScale' function is used to find eyes within the 'roi_gray'(the faceregion).
    eyes = eye_cascade.detectMultiScale(roi_gray)

    # draw a rectangle around eyes
    # For each detected eye, a yellow rectangle is drawn around it in the 'roi_color'(colored face).
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 255), 2)

# display the image with detected eyes
cv2.imshow('Eyes Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()