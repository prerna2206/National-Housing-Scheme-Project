import os
import re
import csv
from pathlib import Path

txt_files_folder = r"\txt_files"
csv_output_folder = r"\csv_data"

os.makedirs(csv_output_folder, exist_ok=True)

SEARCH_TERMS = {
    "Public Housing": r"public\s*-?\s*housing",
    "Rent Supplement": r"rent\s*-?\s*supplement",
    "Limited dividend": r"limited\s*-?\s*dividend",
    "Sect 26/27": r"sect(?:ion)?\.?\s*-?\s*(?:26[\s/-]+27|26/?27)",
    "Sect 95 - PNP": r"sect(?:ion)?\.?\s*-?\s*95\s*-?\s*(?:p\.?\s*n\.?\s*p|pnp)",
    "Sect 95 - MNP": r"sect(?:ion)?\.?\s*-?\s*95\s*-?\s*(?:m\.?\s*n\.?\s*p|mnp)",
    "Provincial reformed": r"provincial\s*-?\s*reformed",
    "Pre-86 urban native": r"pre\s*-?\s*86\s*-?\s*urban\s*-?\s*native",
    "Post 85 urban native": r"post\s*-?\s*85\s*-?\s*urban\s*-?\s*native"
}

def extract_year_from_filename(filename):
    """Extract 4 consecutive digits from filename"""
    match = re.search(r'\d{4}', filename)
    return match.group() if match else ""

def extract_city_from_path(file_path):
    """Extract city name from folder path (removing numbers and spaces)"""
    parent_dir = os.path.dirname(file_path)
    folder_name = os.path.basename(parent_dir)
    if folder_name == "txt_files":
        return ""
    return re.sub(r'[\d\s]', '', folder_name)

def get_bounded_content(content):
    """
    Extract content between the first and second "Social Housing" occurrences.
    Returns None if boundaries aren't found.
    """
    social_housing_pattern = r'^\s*Social\s+Housing\s*$'
    
    social_housing_matches = [match.start() for match in re.finditer(social_housing_pattern, content, re.IGNORECASE | re.MULTILINE)]
    
    if len(social_housing_matches) < 2:
        return None
    
    bounded_content = content[social_housing_matches[0]:social_housing_matches[1]]
    return bounded_content

def extract_number_for_term(bounded_content, term_pattern):
    """
    Extract number following the term if it appears alone on its line.
    Returns empty string if no valid number is found.
    """
    if not bounded_content:
        return ""
        
    content_lines = bounded_content.split('\n')
    
    for i, line in enumerate(content_lines):
        if re.search(term_pattern, line, re.IGNORECASE):
    
            for next_line in content_lines[i+1:]:
                if not next_line.strip():
                    continue
                number_match = re.match(r'^\s*(\d+)\s*$', next_line)
                if number_match:
                    return number_match.group(1)
                elif re.match(r'^\s*U\s*$', next_line):
                    return "0"
                else:
                    break
            break
    
    return ""

csv_path = os.path.join(csv_output_folder, 'housing_data.csv')
headers = ['Year', 'City'] + list(SEARCH_TERMS.keys())

with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    
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
                    
                    row_data = {
                        'Year': year,
                        'City': city
                    }
                    
                    for column_name in SEARCH_TERMS.keys():
                        row_data[column_name] = ""
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    bounded_content = get_bounded_content(content)
                    
                    if bounded_content:
                        for column_name, term_pattern in SEARCH_TERMS.items():
                            number = extract_number_for_term(bounded_content, term_pattern)
                            row_data[column_name] = number
                    
                    writer.writerow(row_data)
                    
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")
                    if os.path.dirname(file_path) != txt_files_folder:
                        row_data = {
                            'Year': extract_year_from_filename(file),
                            'City': extract_city_from_path(file_path)
                        }
                        for column_name in SEARCH_TERMS.keys():
                            row_data[column_name] = ""
                        writer.writerow(row_data)

print(f"CSV file has been created at: {csv_path}")
