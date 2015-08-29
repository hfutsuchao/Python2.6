from pytesser import *
image = Image.open('C:\\Users\\suchao\\Desktop\\2.png')  # Open image object using PIL
print image_to_string(image)     # Run tesseract.exe on image