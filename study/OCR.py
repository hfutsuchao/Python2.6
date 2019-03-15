from pytesser import *

image = Image.open('ocrPic/1.png')  # Open image object using PIL
print image_to_string(image)     # Run tesseract.exe on image
