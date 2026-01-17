import os
import re
from collections import defaultdict

def check_duplicates():
    base_dir = r"d:\python\kisobank\db"
    sql_files = [f for f in os.listdir(base_dir) if f.startswith("sample_data_") and f.endswith(".sql")]
    
    kode_map = defaultdict(list)
    name_map = defaultdict(list)
    
    # Regex to match ('kode', 'nama_produk',
    pattern = re.compile(r"\('([^']+)',\s*'([^']+)',")
    
    for file_name in sql_files:
        if file_name == "sample_data_product.sql":
            continue
        file_path = os.path.join(base_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = pattern.findall(content)
            for kode, name in matches:
                kode_map[kode].append((name, file_name))
                name_map[name].append((kode, file_name))
                
    print("=== DUPLICATE KODE ===")
    found_kode = False
    for kode, occurrences in kode_map.items():
        if len(occurrences) > 1:
            found_kode = True
            print(f"Kode: {kode}")
            for name, file in occurrences:
                print(f"  - {name} ({file})")
    
    if not found_kode:
        print("No duplicate kode found.")
        
    print("\n=== DUPLICATE NAMA PRODUK ===")
    found_name = False
    for name, occurrences in name_map.items():
        if len(occurrences) > 1:
            found_name = True
            print(f"Nama: {name}")
            for kode, file in occurrences:
                print(f"  - {kode} ({file})")
    
    if not found_name:
        print("No duplicate product names found.")

if __name__ == "__main__":
    check_duplicates()
