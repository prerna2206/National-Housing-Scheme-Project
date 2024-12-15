import os
import pandas as pd
import re

def extract_year(filename):
    match = re.search(r'\d{4}', filename)
    return match.group(0) if match else None

def clean_city_name(folder_name):
    return re.sub(r'[\d\s]', '', folder_name)

def create_housing_data_with_programs(root_folder, output_csv):
    data = []
    
    programs = [
        "Public Housing", "Rent Supplement", "Limited Dividend", "Section 26", 
        "Section 27", "Section 95 PNP", "Section 95 MNP", "Provincial Reformed", 
        "Pre-1986 Urban Native", "Post-1985 Urban Native"
    ]
    
    # Walk through all subfolders
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.pdf'):
                year = extract_year(file)
                if year:
                    subfolder = os.path.basename(root)
                    city = clean_city_name(subfolder)
                    
                    for program in programs:
                        row = {
                            'Year': year,
                            'City': city,
                            'Name': program,
                            'RGI': '',
                            'Non-RGI': '',
                            'Vacant Units': ''
                        }
                        data.append(row)
    
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)

input_folder = r"E:\Sem 4\SMAIR 1"
output_csv = r"E:\Sem 4\csv_data\housing_data_page_4_part1.csv"
create_housing_data_with_programs(input_folder, output_csv)
