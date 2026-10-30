import os
import pytesseract

from PIL import Image
from werkzeug.utils import secure_filename


# Tesseract OCR ka path
# Agar Tesseract install hai aur PATH mein added hai,
# toh is line ko comment bhi kar sakte ho.
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text_from_image(file_path):
    """
    Image file se text extract karta hai.
    """

    if not os.path.exists(file_path):
        return {
            "success": False,
            "text": "",
            "message": "File not found."
        }

    try:
        image = Image.open(file_path)

        extracted_text = pytesseract.image_to_string(
            image
        )

        return {
            "success": True,
            "text": extracted_text,
            "message": "Text extracted successfully."
        }

    except Exception as error:
        return {
            "success": False,
            "text": "",
            "message": str(error)
        }


def is_supported_file(filename):
    """
    Check karta hai ki file supported hai ya nahi.
    """

    allowed_extensions = {
        "png",
        "jpg",
        "jpeg",
        "bmp",
        "tiff"
    }

    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in allowed_extensions