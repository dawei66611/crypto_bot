import pytesseract
from PIL import Image
import io

def perform_ocr(image_data):
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    return text

