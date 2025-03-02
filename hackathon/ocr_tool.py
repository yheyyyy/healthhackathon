from PIL import Image
import easyocr

# OCR function for EasyOCR integration
def ocr_tool_function(image) -> str:
    ocr_reader = easyocr.Reader(['en']) 
    """Extract text from image using EasyOCR."""
    image = Image.open(image)
    ocr_result = ocr_reader.readtext(image)
    extracted_text = ' '.join([text[1] for text in ocr_result])
    return extracted_text
