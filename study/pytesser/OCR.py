from pytesser import *

image = Image.open('/Users/NealSu/GoogleDisk/MyTools/Python2.6/study/pytesser/phototest.tif')  # Open image object using PIL
print image_to_string(image)     # Run tesseract.exe on image
