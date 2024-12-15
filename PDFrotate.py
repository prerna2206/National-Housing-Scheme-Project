import os
from PyPDF2 import PdfReader, PdfWriter

def rotate_pages_in_pdf(pdf_path, pages_to_rotate, rotation_angle):
    """
    Rotates specific pages in a PDF file and saves the result.

    :param pdf_path: Path to the PDF file.
    :param pages_to_rotate: List of page numbers to rotate (1-based indexing).
    :param rotation_angle: The angle by which to rotate the pages (positive for clockwise, negative for anti-clockwise).
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        if (page_num + 1) in pages_to_rotate:
            page.rotate(rotation_angle)
        
        writer.add_page(page)

    with open(pdf_path, 'wb') as f:
        writer.write(f)

def process_pdfs(base_folder, operations):
    """
    Processes the PDFs as per the operations provided.
    
    :param base_folder: The root folder where subfolders and PDFs are located.
    :param operations: Dictionary containing subfolder names, file names, and page rotation instructions.
    """
    for subfolder, files in operations.items():
        subfolder_path = os.path.join(base_folder, subfolder)
        for pdf_file, rotation_info in files.items():
            pdf_path = os.path.join(subfolder_path, pdf_file)
            for pages, angle in rotation_info:
                
                rotate_pages_in_pdf(pdf_path, pages, angle)

operations = {
    "04 Chatham-Kent": {
        "SMAIR 2015 Chatham-Kent.pdf": [([3, 4, 5, 6], 90)],
    },
    "16 Kingston": {
        "SMAIR 2011 - City of Kingston.pdf": [([3, 4, 7, 8, 9], -90)],
        "SMAIR 2012 - City of Kingston.pdf": [([3, 4, 7, 8, 9], 90)],
        "SMAIR 2013 - City of Kingston.pdf": [([3, 4, 7, 8, 9], 90)],
        "SMAIR 2014 - City of Kingston.pdf": [([4, 5, 6, 7], 90)],
        "SMAIR 2015 - City of Kingston.pdf": [([3, 4, 5, 6], 90)],
        "SMAIR 2016 - City of Kingston.pdf": [([3, 4, 5, 6], 90)],
        "SMAIR 2017 - City of Kingston.pdf": [([5, 6, 7, 8, 9], 90)],
        "SMAIR 2018 - City of Kingston.pdf": [([11, 12, 13, 14, 15, 16], 90)],
        "SMAIR 2019.pdf": [([5, 6, 7, 8, 9, 10], 90)],
    },
    "29 Ottawa": {
        "A-2024-00230 - Release Package.pdf": [([99], -90), ([249, 252], 90)],
    },
    "33 Peterborough": {
        "City SMAIRs 2017-2021.pdf": [([5, 6, 7, 8, 9, 14, 15, 16, 17, 18, 24, 25, 26, 27, 28, 29, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 51, 52, 53, 54, 55, 56, 57, 58, 59], 90)],
    },
    "47 York": {
        "SMAIR 2011.pdf": [([4, 5, 8, 9], 90)],
        "SMAIR 2012.pdf": [([4, 5, 6, 7, 8, 9], 90)],
        "SMAIR 2013.pdf": [([5, 6, 9, 11], 90)],
        "SMAIR 2014.pdf": [([5, 6, 7, 9], 90)],
        "SMAIR 2015.pdf": [([4, 5, 6, 7], 90)],
        "SMAIR 2016.pdf": [([4, 5, 6, 7], 90)],
        "SMAIR 2017.pdf": [([7, 8, 9, 10, 11, 12, 15], 90)],
        "SMAIR 2018.pdf": [([5, 6, 7, 8, 9], 90)],
        "SMAIR 2019.pdf": [([5, 6, 7, 8, 9, 10], 90)],
    }
}

base_folder = r"\SMAIR 1"

process_pdfs(base_folder, operations)

print("PDF page rotations complete.")
