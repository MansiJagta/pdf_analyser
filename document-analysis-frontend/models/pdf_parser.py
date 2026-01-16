import fitz  # PyMuPDF
from paddleocr import PaddleOCR

class PDFParser:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, show_log=False)

    def extract_text(self, file_path):
        doc = fitz.open(file_path)
        text_output = ""
        for page in doc:
            page_text = page.get_text()
            # If the page is mostly an image (scan), run OCR
            if len(page_text.strip()) < 50:
                img_list = page.get_images()
                if img_list:
                    result = self.ocr.ocr(file_path, cls=True)
                    page_text = "\n".join([line[1][0] for line in result[0]])
            text_output += page_text + "\n"
        return text_output