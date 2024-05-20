import cv2

# Load the images
image1 = cv2.imread('image1.jpg')
image2 = cv2.imread('image2.jpg')

# Initialize the SIFT feature detector and extractor
sift = cv2.ORB_create()

# Detect keypoints and compute descriptors for both images
keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

# Draw keypoints on the images
image1_keypoints = cv2.drawKeypoints(image1, keypoints1, None)
image2_keypoints = cv2.drawKeypoints(image2, keypoints2, None)

# Display the images with keypoints
cv2.imshow('Image 1 with Keypoints', image1_keypoints)
cv2.imshow('Image 2 with Keypoints', image2_keypoints)
cv2.imwrite("keypoints_1.jpg", image1_keypoints)
cv2.imwrite("keypoints_2.jpg", image2_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()