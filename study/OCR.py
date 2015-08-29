from pytesser import *

image = Image.open('ocrPic/QQ20150711-1@2x.png')  # Open image object using PIL
print image_to_string(image)     # Run tesseract.exe on image
