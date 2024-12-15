import os
import re
import csv

txt_files_folder = r"\txt_files"
csv_output_folder = r"\csv_data"

os.makedirs(csv_output_folder, exist_ok=True)

def extract_year_from_filename(filename):
    """Extract 4 consecutive digits from filename."""
    match = re.search(r'\d{4}', filename)
    return int(match.group()) if match else None

def extract_city_from_path(file_path):
    """Extract city name from folder path (removing numbers and spaces)."""
    parent_dir = os.path.dirname(file_path)
    folder_name = os.path.basename(parent_dir)
    if folder_name == "txt_files":
        return ""
    return re.sub(r'[\d\s]', '', folder_name)

def split_content_by_page(content):
    """Split content by 'PageX' headers and return as list of pages."""
    pages = re.split(r'^\s*(Page\s*[0-9A-Za-z]*)\s*', content, flags=re.MULTILINE)
    return [pages[i + 1] for i in range(1, len(pages), 2)]

def extract_page_5_data(page_5_content, year):
    """
    Extract table data for 'Total SHRRP Funding Received' and 'Total Expenditures'
    based on the year:
    - If year <= 2011, split at "SHRRP".
    - If 2012 <= year <= 2013, take all content from Page 5.
    """
    if year <= 2011:
        split_page_5 = page_5_content.split("SHRRP", 1)
        if len(split_page_5) < 2:
            return [""] * 4, [""] * 4 
        after_shrrp_content = split_page_5[1].splitlines()
    else:
        after_shrrp_content = page_5_content.splitlines()

    first_row = ["Total SHRRP Funding Received", None, None, None]
    second_row = ["Total Expenditures", None, None, None]

    def find_values_in_line(line):
    
        if re.match(r'^\s*(\$\d{1,3}(?:,\d{3})*|\d+|SO)\s*$', line):
            return re.findall(r'(\$\d{1,3}(?:,\d{3})*|\d+|SO)', line)
        return []

    for i, line in enumerate(after_shrrp_content):
        line = line.strip()
        if "Total SHRRP Funding Received" in line:
            values = find_values_in_line(line)
            if not values:
                next_line = after_shrrp_content[i + 1].strip()
                values = find_values_in_line(next_line)
            first_row[3] = values[0] if values else ""
        elif "Total Expenditures" in line:
            values = find_values_in_line(line)
            if len(values) < 3:
                next_lines = [after_shrrp_content[i + j].strip() for j in range(1, 4)]
                for next_line in next_lines:
                    next_line_values = find_values_in_line(next_line)
                    if next_line_values:
                        values.extend(next_line_values)
                    if len(values) >= 3:
                        break
            second_row[1:4] = values[:3]

    return first_row, second_row

csv_path = os.path.join(csv_output_folder, 'page_5_data.csv')
headers = ['Year', 'City', 'Category', 'Repair', 'Regeneration', 'Total']

with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)

    for root, dirs, files in os.walk(txt_files_folder):
        for file in files:
            if file.lower().endswith('.txt'):
                file_path = os.path.join(root, file)
                if os.path.dirname(file_path) == txt_files_folder:
                    continue

                try:
                    year = extract_year_from_filename(file)
                    if year is None or year > 2013:
                        continue

                    city = extract_city_from_path(file_path)
                    if not city:
                        continue

                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    pages = split_content_by_page(content)

                    if len(pages) >= 5:
                        page_5_content = pages[4]
                        first_row, second_row = extract_page_5_data(page_5_content, year)

                        writer.writerow([year, city] + first_row)
                        writer.writerow([year, city] + second_row)

                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")

print(f"CSV file has been created at: {csv_path}")
