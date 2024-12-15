import os
import re
import csv
from pathlib import Path

txt_files_folder = r"E:\Sem 4\txt_files"
csv_output_folder = r"E:\Sem 4\csv_data"

def extract_year_city(filename, folder_path):
    try:
        year_match = re.search(r'(\d{4})', filename)
        year = year_match.group(1) if year_match else None

        # Extract city name from the folder path
        city = os.path.basename(folder_path).strip()
        city = re.sub(r'\d+', '', city)

        return year, city.strip()
    except Exception as e:
        print(f"Error extracting year and city from filename {filename}: {str(e)}")
        return None, None

def extract_public_housing(content):
    try:
        start_match = re.search(r'2151', content)
        if not start_match:
            return None

        end_match = re.search(r'2154', content[start_match.end():])
        if not end_match:
            return None
        relevant_content = content[start_match.end():start_match.end() + end_match.start()]

        number_match = re.search(r'\d+', relevant_content)
        if number_match:
            return number_match.group(0)
        return None

    except Exception as e:
        print(f"Error extracting public housing number: {str(e)}")
        return None

def process_files():

    os.makedirs(csv_output_folder, exist_ok=True)

    output_file = os.path.join(csv_output_folder, 'service_lvl.csv')

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['Year', 'City', 'Public Housing'])

        for root, dirs, files in os.walk(txt_files_folder):
            for file in files:
                if file.lower().endswith('.txt'):
                    file_path = os.path.join(root, file)
                    try:
                        
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        year, city = extract_year_city(file, root)

                        public_housing = extract_public_housing(content)

                        if year and city and public_housing:
                            writer.writerow([year, city, public_housing])
                            print(f"Successfully processed: {file}")
                        else:
                            print(f"Incomplete data for file {file}")
                            if not year:
                                print("  - Could not extract year")
                            if not city:
                                print("  - Could not extract city")
                            if not public_housing:
                                print("  - Could not extract public housing number")

                    except Exception as e:
                        print(f"Error processing file {file}: {str(e)}")

def main():
    print("Starting data extraction...")
    process_files()
    print(f"Data extraction completed. Results saved to {os.path.join(csv_output_folder, 'service_lvl.csv')}")

if __name__ == "__main__":
    main()