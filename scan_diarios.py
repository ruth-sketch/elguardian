import os
import json

def scan_diarios(base_path):
    # Load existing metadata (categories and portadas)
    metadata = {}
    for filename in ['diarios.json']:
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    old_data = json.load(f)
                    for item in old_data:
                        name = item.get('name')
                        if name:
                            name_lower = name.lower()
                            if name_lower not in metadata:
                                metadata[name_lower] = {}
                            if item.get('categoria'):
                                metadata[name_lower]['categoria'] = item.get('categoria')
                            if item.get('portada'):
                                metadata[name_lower]['portada'] = item.get('portada')
            except Exception as e:
                print(f"Warning: Error loading {filename}: {e}")

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
                name_lower = folder_name.lower()
                diario_item = {
                    "name": folder_name,
                }
                
                # Merge metadata
                categoria = metadata.get(name_lower, {}).get('categoria')
                if not categoria:
                    categoria = "actualidad"
                diario_item["categoria"] = categoria
                
                portada = metadata.get(name_lower, {}).get('portada')
                if portada:
                    diario_item["portada"] = portada
                
                diario_item["tomos"] = tomo_files
                diarios.append(diario_item)
    
    # Custom Sort: 'el guardian' 1st, 'el universo' 2nd, 'el observador' 3rd, then rest alphabetically
    priority = {
        'el guardian': 0,
        'el universo': 1,
        'el observador': 2,
        'el guardian ii': 1000  # Put it last
    }
    
    diarios.sort(key=lambda x: (priority.get(x['name'].lower(), 99), x['name'].lower()))
    
    return diarios

if __name__ == "__main__":
    # Use the directory where the script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data = scan_diarios(base_dir)
    with open(os.path.join(base_dir, 'diarios.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Generated diarios.json with {len(data)} diarios.")
