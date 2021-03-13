"""
Program to extract the number of license plate of a Car
Date: 03/13/2021
"""

# Loading the required python modules
import pytesseract
pytesseract.pytesseract.tesseract_cmd=r'C:\Users\luisenrique\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
import matplotlib.pyplot as plt
import cv2
import glob
import os
import wget, zipfile, os


filename='license-plates'

if not os.path.isfile(filename):
    filename = wget.download('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/CV0101/Dataset/license-plates.zip')
    with zipfile.ZipFile("license-plates.zip","r") as zip_ref:
        zip_ref.extractall()


path_for_license_plates = os.getcwd() + "/license-plates/**/*.jpg"
path_for_license_plates=path_for_license_plates.replace("\\","/")
print(path_for_license_plates)
list_license_plates = []
predicted_license_plates = []

for path_to_license_plate in glob.glob(path_for_license_plates, recursive=True):

    license_plate_file_fixed= path_to_license_plate.replace("\\","/")
    license_plate_file = license_plate_file_fixed.split("/")[-1]
    license_plate, _ = os.path.splitext(license_plate_file)
    print(license_plate)
    '''
    Here we append the actual license plate to a list
    '''
    list_license_plates.append(license_plate)

    '''
    Read each license plate image file using openCV
    '''
    #print(path_to_license_plate)
    img = cv2.imread(path_to_license_plate)
    cv2.imshow("plate", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    '''
    We then pass each license plate image file to the Tesseract OCR engine using
    the Python library wrapper for it. We get back a predicted_result for the license plate.
    We append the predicted_result in a list and compare it with the original the license plate
    '''
    predicted_result = pytesseract.image_to_string(img, lang='eng',
    config='--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    filter_predicted_result = "".join(predicted_result.split()).replace(":", "").replace("-", "")
    predicted_license_plates.append(filter_predicted_result)

print("Actual License Plate", "\t", "Predicted License Plate", "\t", "Accuracy")
print("--------------------", "\t", "-----------------------", "\t", "--------")

def calculate_predicted_accuracy(actual_list, predicted_list):
    for actual_plate, predict_plate in zip(actual_list, predicted_list):
        accuracy = "0%"
        num_matches = 0
        if actual_plate == predict_plate:
            accuracy = "100%"
        else:
            if len(actual_plate) == len(predict_plate):
                for a, p in zip(actual_plate, predict_plate):
                    if a == p:
                        num_matches += 1
                accuracy = str(round((num_matches/len(actual_plate)), 2) * 100)
                accuracy += "%"
        print("     ", actual_plate, "\t\t\t", predict_plate, "\t\t  ", accuracy)


calculate_predicted_accuracy(list_license_plates, predicted_license_plates)

"""
EXCERCISE 1.

# Read the license plate file and display it
test_license_plate = cv2.imread(os.getcwd() + "/license-plates/GWT2180.jpg")
plt.imshow(test_license_plate)
plt.axis('off')
plt.title('GWT2180 license plate')
plt.show() 

resize_test_license_plate = cv2.resize(test_license_plate, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
grayscale_resize_test_license_plate = cv2.cvtColor(resize_test_license_plate, cv2.COLOR_BGR2GRAY)
gaussian_blur_license_plate = cv2.GaussianBlur(grayscale_resize_test_license_plate, (5, 5), 0)

new_predicted_result_GWT2180 = pytesseract.image_to_string(gaussian_blur_license_plate, lang='eng',
config='--oem 3 -l eng --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
filter_new_predicted_result_GWT2180 = "".join(new_predicted_result_GWT2180.split()).replace(":", "").replace("-", "")
print("La nueva prediccion es:")
print(filter_new_predicted_result_GWT2180)

"""


#EXCERCISE 2.
# 2.1 Read in the license plate file of FL029RF (the file is in the
# test-plates folder, paste it with the others)
# Write your code below:





# 2.2 Apply the image processing techniques to the license plate of FL029RF described above 
# Write your code below:



# 2.3 Pass the modified license plate file to the Tesseract Engine. Report your findings 
# Write your code below:


