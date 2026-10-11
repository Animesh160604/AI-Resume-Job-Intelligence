import pymupdf
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF.

    First tries normal PDF text extraction.
    If the PDF contains no readable text, OCR is used.
    """

    document = pymupdf.open(pdf_path)

    extracted_text = ""

    # Step 1: Try normal text extraction
    for page in document:
        extracted_text += page.get_text()

    # If text was found, return it
    if extracted_text.strip():
        document.close()
        return extracted_text

    # Step 2: PDF is probably scanned/image-based
    print("No text found. Using OCR...")

    ocr_text = ""

    for page_number, page in enumerate(document):

        print(f"OCR processing page {page_number + 1}...")

        # Render PDF page as an image
        pix = page.get_pixmap(dpi=200)

        # Convert image bytes to PIL image
        image = Image.open(io.BytesIO(pix.tobytes("png")))

        # Perform OCR using Tesseract
        text = pytesseract.image_to_string(image)

        ocr_text += text + "\n"

    document.close()

    return ocr_text


if __name__ == "__main__":

    pdf_path = "phase1/resumes/my_resume.pdf"

    resume_text = extract_text_from_pdf(pdf_path)

    print("\n" + "=" * 70)
    print("EXTRACTED RESUME TEXT")
    print("=" * 70)

    print(resume_text)

    print("=" * 70)