import fitz  # PyMuPDF
import boto3
import os
from sqlalchemy import create_engine

# AWS S3 configuration
s3_bucket = 'your-bucket-name'
s3_client = boto3.client('s3')

# Database configuration (example for PostgreSQL)
db_url = 'postgresql://username:password@hostname/dbname'
engine = create_engine(db_url)

def download_pdf_from_s3(pdf_key):
    s3_client.download_file(s3_bucket, pdf_key, 'downloaded.pdf')

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def update_db_with_extracted_text(pdf_key, extracted_text):
    connection = engine.connect()
    connection.execute("UPDATE pdfs SET extracted_text = %s WHERE s3_key = %s", (extracted_text, pdf_key))
    connection.close()

if __name__ == "__main__":
    pdf_key = 'path/to/your.pdf'  # Replace with your PDF key in S3
    download_pdf_from_s3(pdf_key)
    extracted_text = extract_text_from_pdf('downloaded.pdf')
    update_db_with_extracted_text(pdf_key, extracted_text)
    os.remove('downloaded.pdf')
    print("Text extracted and updated in the database")
