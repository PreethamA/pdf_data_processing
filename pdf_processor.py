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

def extract_metadata_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    metadata = doc.metadata
    return metadata

def extract_images_from_pdf(pdf_path, output_dir='images'):
    doc = fitz.open(pdf_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    image_files = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = os.path.join(output_dir, f"image_{page_num + 1}_{img_index + 1}.{image_ext}")
            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)
            image_files.append(image_filename)
    return image_files

def update_db_with_extracted_data(pdf_key, extracted_text, metadata):
    connection = engine.connect()
    connection.execute(
        "UPDATE pdfs SET extracted_text = %s, metadata = %s WHERE s3_key = %s",
        (extracted_text, metadata, pdf_key)
    )
    connection.close()

if __name__ == "__main__":
    pdf_key = 'path/to/your.pdf'  # Replace with your PDF key in S3
    download_pdf_from_s3(pdf_key)
    extracted_text = extract_text_from_pdf('downloaded.pdf')
    metadata = extract_metadata_from_pdf('downloaded.pdf')
    image_files = extract_images_from_pdf('downloaded.pdf')
    
    # Serialize metadata to a string for database storage
    metadata_str = str(metadata)
    
    update_db_with_extracted_data(pdf_key, extracted_text, metadata_str)
    
    # Clean up downloaded PDF and extracted images
    os.remove('downloaded.pdf')
    for image_file in image_files:
        os.remove(image_file)
    
    print("Text, metadata, and images extracted and updated in the database")
