import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

if __name__ == "__main__":
    pdf_path = "sample.pdf"  # Replace with your PDF file path
    extracted_text = extract_text_from_pdf(pdf_path)
    with open("extracted_text.txt", "w") as text_file:
        text_file.write(extracted_text)
    print("Text extracted and saved to extracted_text.txt")
