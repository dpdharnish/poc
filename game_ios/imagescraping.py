import cv2
import pytesseract
import re
import numpy as np
# Load the image using OpenCV
def extract(path):
    image = cv2.imread(path)

    # Define the lower and upper bounds of the sky blue color in BGR format
    lower_blue = np.array([100, 150, 200])
    upper_blue = np.array([255, 255, 255])

    # Create a mask to isolate the sky blue regions in the image
    mask = cv2.inRange(image, lower_blue, upper_blue)

    # Bitwise-AND the mask and the original image to keep only the sky blue regions
    blue_regions = cv2.bitwise_and(image, image, mask=mask)

    # Convert the blue regions to grayscale
    gray = cv2.cvtColor(blue_regions, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to enhance text
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Use Pytesseract to extract text from the preprocessed image
    extracted_text = pytesseract.image_to_string(thresholded)

    # Define a regular expression pattern to extract whole numbers (integers)
    number_pattern = r'[-+]?\d+'

    # Find all whole numbers in the extracted text and join them in one line
    numbers = ''.join(re.findall(number_pattern, extracted_text))
    l = len(numbers)
    if l<=6:
        print("Score is:",numbers)
    else:
        print("Score is:",numbers[l-6:])
