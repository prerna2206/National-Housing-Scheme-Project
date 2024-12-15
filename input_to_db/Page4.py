import os
import re

txt_files_folder = r"E:\Sem 4\txt_files"

pattern_csi = r'(?i)Combined\s*Statistical\s*Information'
pattern_social_housing = r'(?i)^\s*Social\s*Housing\s*$'
pattern_page_4 = r'(?i)^\s*Page\s*4\s*$'

def get_page_4_boundaries(content):
    csi_matches = list(re.finditer(pattern_csi, content))
    page_4_matches = list(re.finditer(pattern_page_4, content))
    
    if not csi_matches:
        return None, None

    if len(csi_matches) == 1:
        
        start = csi_matches[0].start()
        social_housing_match = re.search(pattern_social_housing, content[start:])
        if social_housing_match:
            end = start + social_housing_match.start()
        else:
            end = len(content)
            
    elif len(csi_matches) == 2:
        
        start = csi_matches[0].start()
        end = csi_matches[1].start()
        
    elif len(csi_matches) == 3:
        
        if len(page_4_matches) >= 2:
            start = page_4_matches[0].end()
            end = page_4_matches[1].start()
        else:
            return None, None
    else:
        return None, None
        
    return start, end

def count_2101_in_page_4(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            start, end = get_page_4_boundaries(content)
            
            if start is None or end is None:
                return None
                
            page_4_content = content[start:end]
            
            return len(re.findall(r'2101', page_4_content))
            
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

def main():
    files_with_2101 = []
    files_without_2101 = []
    
    for root, dirs, files in os.walk(txt_files_folder):
        for file in files:
            if file.lower().endswith('.txt'):
                file_path = os.path.join(root, file)
                count = count_2101_in_page_4(file_path)
                
                if count is not None:
                    if count > 0:
                        files_with_2101.append((file_path, count))
                    else:
                        files_without_2101.append(file_path)
    
    print("\nFiles containing '2101' in Page 4:")
    for file_path, count in files_with_2101:
        print(f"{file_path} - {count} occurrences")
    
    print("\nFiles without '2101' in Page 4:")
    for file_path in files_without_2101:
        print(file_path)

if __name__ == "__main__":
    main()