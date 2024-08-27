import PyPDF2

def extract_text(file_path: str) -> str:
    """
    Extracts text from a PDF file and returns the specified number of characters.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text.
    """
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''

    for page in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page]
        text += page_obj.extract_text()

    pdf_file.close()
    return text
