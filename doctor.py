import os
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

model = ocr_predictor(det_arch="db_resnet50", reco_arch="parseq", pretrained=True)

input_folder = r"E:/Sem 4/SMAIR 1"
output_folder = r"E:/Sem 4/txt_files"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def process_pdf(pdf_path, output_path):
    try:

        pdf_doc = DocumentFile.from_pdf(pdf_path)

        result = model(pdf_doc)

        extracted_text = ""
        for page in result.pages:
            for block in page.blocks:
                for line in block.lines:
                    for word in line.words:
                        extracted_text += word.value + " "
                    extracted_text += "\n"
                extracted_text += "\n"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print(f"Text extracted and saved to {output_path}")
    
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")

for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(root, file)
            
            relative_path = os.path.relpath(pdf_path, input_folder)
            output_subfolder = os.path.join(output_folder, os.path.dirname(relative_path))

            if not os.path.exists(output_subfolder):
                os.makedirs(output_subfolder)

            output_txt_path = os.path.join(output_subfolder, os.path.splitext(file)[0] + ".txt")

            process_pdf(pdf_path, output_txt_path)
