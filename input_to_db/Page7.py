import os
import re
import csv

txt_files_folder = r"\txt_files"
csv_output_folder = r"\csv_data"

os.makedirs(csv_output_folder, exist_ok=True)

def extract_year_from_filename(filename):
    match = re.search(r'\d{4}', filename)
    return match.group() if match else ""

def extract_city_from_path(file_path):
    parent_dir = os.path.dirname(file_path)
    folder_name = os.path.basename(parent_dir)
    if folder_name == "txt_files":
        return ""
    return re.sub(r'[\d\s]', '', folder_name)

def process_page_7_content(content):
    pages = re.split(r'^\s*(Page\s*[0-9A-Za-z]*)\s*', content, flags=re.MULTILINE)
    page_7_content = None

    for i in range(1, len(pages), 2):
        if pages[i].strip() in ["Page7", "Page 7"]:
            page_7_content = pages[i + 1] if i + 1 < len(pages) else None
            break  # Stop after finding Page 7

    if not page_7_content:
        return []

    data = {
        "Number of households receiving PHB": {
            "Unit of Measurement": "Households", "Families": "", "Seniors": "", "Non-elderly Singles": "", "Total": ""
        },
        "Average Adjusted Family Net Income (AFNI)": {
            "Unit of Measurement": "$", "Families": "", "Seniors": "", "Non-elderly Singles": "", "Total": ""
        },
        "Municipal expenditures for PHB": {
            "Unit of Measurement": "$", "Families": "", "Seniors": "", "Non-elderly Singles": "", "Total": ""
        },
        "Households with income at/below HIL": {
            "Unit of Measurement": "Households", "Families": "", "Seniors": "", "Non-elderly Singles": "", "Total": ""
        },
        "High-need households receiving PHB": {
            "Unit of Measurement": "Households", "Families": "", "Seniors": "", "Non-elderly Singles": "", "Total": ""
        }
    }

    predefined_numbers = {
        "2111": ("Families", 0),               # Number of households receiving PHB
        "2113": ("Families", 1),               # Average Adjusted Family Net Income (AFNI)
        "2121": ("Seniors", 0),                # Number of households receiving PHB
        "2123": ("Seniors", 1),                # Average Adjusted Family Net Income (AFNI)
        "2131": ("Non-elderly Singles", 0),    # Number of households receiving PHB
        "2133": ("Non-elderly Singles", 1),    # Average Adjusted Family Net Income (AFNI)
        "2151": ("Total", 0),                  # Number of households receiving PHB
        "421": ("Total", 2),                   # Municipal expenditures for PHB
        "2161": ("Total", 3),                  # Households with income at/below HIL
        "2162": ("Total", 4)                   # High-need households receiving PHB
    }

    value_pattern = re.compile(r'\b(\$?\d{1,3}(?:,\d{3})*(?:\.\d+)?)\b')

    current_number = None

    for line in page_7_content.splitlines():
        line = line.strip()
        if not line:
            continue

        for number in predefined_numbers.keys():
            if number in line:

                column, row = predefined_numbers[number]
                current_number = number
                break

        if current_number:
            matches = value_pattern.findall(line)
            if matches:

                row_name = list(data.keys())[row]
                data[row_name][column] = matches[0]
                current_number = None

    output_data = []
    for category, values in data.items():
        output_data.append([category, values["Unit of Measurement"], values["Families"], 
                            values["Seniors"], values["Non-elderly Singles"], values["Total"]])

    return output_data

csv_path_page_7 = os.path.join(csv_output_folder, 'page_7.csv')
columns = ['Year', 'City', 'Category', 'Unit of Measurement', 'Families', 'Seniors', 'Non-elderly Singles', 'Total']

with open(csv_path_page_7, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(columns)

    for root, dirs, files in os.walk(txt_files_folder):
        for file in files:
            if file.lower().endswith('.txt'):
                file_path = os.path.join(root, file)
                if os.path.dirname(file_path) == txt_files_folder:
                    continue

                try:
                    year = extract_year_from_filename(file)
                    city = extract_city_from_path(file_path)
                    if not city:
                        continue
                    
                    if not (2017 <= int(year) <= 2021):
                        continue
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    extracted_data = process_page_7_content(content)

                    for row in extracted_data:
                        writer.writerow([year, city] + row)

                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")

print(f"CSV file for Page 7 has been created at: {csv_path_page_7}")
