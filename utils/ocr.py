# utils/ocr.py

import pytesseract
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

def perform_ocr(image_data):
    try:
        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image, lang='chi_sim')  # 使用中文语言包
        return text
    except Exception as e:
        logger.error(f"OCR 识别失败: {e}")
        return ""
