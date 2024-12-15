import os
import csv

csv_folder = r"\csv_data"

def format_numeric_cells(value):
    # Handle empty or missing values
    if value == "":
        return "0.00"
    
    value = value.replace("$", "").replace(",", "").replace("%", "")
    try:
        return f"{float(value):.2f}"
    except ValueError:
        return value

for csv_file in os.listdir(csv_folder):
    if csv_file.lower().endswith('.csv'):
        csv_path = os.path.join(csv_folder, csv_file)
        
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        for i in range(1, len(rows)):
            for j in range(len(rows[i])):
                rows[i][j] = format_numeric_cells(rows[i][j])

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print(f"Formatted CSV file: {csv_file}")

print("All CSV files have been formatted")
