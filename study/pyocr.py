try: 
    import Image 
except ImportError: 
    from PIL import Image 
import pytesseract 
print(pytesseract.image_to_string(Image.open('ocrPic/1.png'))) 
print(pytesseract.image_to_string(Image.open('ocrPic/1.png'), lang='fra'))
