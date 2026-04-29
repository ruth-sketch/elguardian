import os
import json

def scan_diarios(base_path):
    diarios = []
    diarios_dir = os.path.join(base_path, 'diarios')
    
    if not os.path.exists(diarios_dir):
        return diarios

    # Iterate through each folder in 'diarios'
    for folder_name in sorted(os.listdir(diarios_dir)):
        folder_path = os.path.join(diarios_dir, folder_name)
        
        if os.path.isdir(folder_path):
            tomo_files = []
            # Iterate through files in the diario folder
            for file_name in sorted(os.listdir(folder_path)):
                if file_name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                    tomo_files.append({
                        "name": file_name,
                        "path": f"diarios/{folder_name}/{file_name}"
                    })
            
            if tomo_files:
                diarios.append({
                    "name": folder_name,
                    "tomos": tomo_files
                })
    
    return diarios

if __name__ == "__main__":
    # Use the directory where the script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data = scan_diarios(base_dir)
    with open(os.path.join(base_dir, 'diarios.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Generated diarios.json with {len(data)} diarios.")
