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

def process_page_3_content(content):
    pages = re.split(r'^\s*(Page\s*[0-9A-Za-z]*)\s*', content, flags=re.MULTILINE)
    page_3_content = None

    for i in range(1, len(pages), 2):
       if pages[i].strip() == "Page3" or pages[i].strip() == "Page 3":
        page_3_content = pages[i + 1] if i + 1 < len(pages) else None
        break

    if not page_3_content:
        return []

    lines_page_3 = page_3_content.splitlines()
    section_headings = [
        "Public housing", "Rent supplement", "Limited dividend", "Section 26",
        "Section 27", "Section 95 - PNP", "Section 95 - MNP", "Provincial reformed",
        "Pre-86 urban native", "Post 85 urban native", "TOTAL"
    ]

    table_data = []
    current_row = []
    collect_values = False

    for line in lines_page_3:
        line = line.strip()
        
        if any(heading in line for heading in section_headings):
            if current_row:
                while len(current_row) < 6:
                    current_row.append(None)
                table_data.append(current_row)
            current_name = next((heading for heading in section_headings if heading in line), "")
            current_row = [current_name]
            collect_values = True

        elif re.match(r'^(411|412|413|414|415|416|417|418|419|420|425)', line):
            parts = re.split(r'[\s\t]+', line)
            if len(current_row) == 1:
                current_row.append(parts[0])  
                parts = parts[1:]
            
            for part in parts:
                
                if re.match(r'^\$?[0-9,]+(\.\d{1,2})?$', part):
                    if len(current_row) < 5:
                        current_row.append(part)
                    else:
                        
                        break  
                elif '%' in part or part == "#DIV/0!":
                    while len(current_row) < 5: 
                        current_row.append(None)
                    current_row.append(part)  
                    table_data.append(current_row)  
                    current_row = [] 
                    collect_values = False
                    break

        elif collect_values and re.search(r'^\d|,|\.', line):
            parts = re.split(r'[\s\t]+', line) 
            for part in parts:
                
                if re.match(r'^\$?[0-9,]+(\.\d{1,2})?$', part):
                    if len(current_row) < 5:
                        current_row.append(part)
                elif '%' in part or part == "#DIV/0!":
                    while len(current_row) < 5:
                        current_row.append(None)
                    current_row.append(part)
                    table_data.append(current_row) 
                    current_row = [] 
                    collect_values = False
                    break
                elif re.search(r'[a-zA-Z]', part): 
                    break

    if current_row:
        while len(current_row) < 6:
            current_row.append(None)
        table_data.append(current_row)

    return table_data, page_3_content

unprocessed_files = []

csv_path_page_3 = os.path.join(csv_output_folder, 'housing_data_page_3.csv')
columns = ['Year', 'City', 'Name', 'Number', 'One Time Funding', 'Ongoing Funding', 'Total', 'Percentage']

with open(csv_path_page_3, 'w', newline='', encoding='utf-8') as csvfile:
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
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    page_3_data, pages = process_page_3_content(content)

                    if city.lower() == "peterborough" and year == "2017":
                        print("Pages content for Peterborough, 2017:")
                        print(pages)

                    for row in page_3_data:
                        writer.writerow([year, city] + row)
                        
                    else:
                        unprocessed_files.append(file)
                
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")

if unprocessed_files:
    print("The following files had no output data and were not processed:")
    for unprocessed_file in unprocessed_files:
        print(unprocessed_file)
else:
    print("All files were processed successfully.")

print(f"CSV file for Page 3 has been created at: {csv_path_page_3}")
