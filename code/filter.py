import cv2

frame = cv2.imread("../img/papas.jpg")

kernel_size = (7,7)
blur = cv2.GaussianBlur(frame, kernel_size, 0)

#############################
#TO-DO apply multiple filters
for i in range(25):
    blur = cv2.GaussianBlur(blur, kernel_size, 0)
#############################

cv2.imshow("Frame", frame)
cv2.imshow("Blur", blur)
cv2.waitKey(0)
cv2.destroyAllWindows()
