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
                if not categoria or name_lower == 'edicion_02_julio_26':
                    if 'guardian' in name_lower or name_lower.startswith('edicion_'):
                        categoria = "ciencia"
                    else:
                        categoria = "actualidad"
                diario_item["categoria"] = categoria
                
                titulo = metadata.get(name_lower, {}).get('titulo')
                if not titulo:
                    if name_lower == 'el guardian':
                        titulo = "Edición N.º 1 – Abril 2026"
                    elif name_lower == 'edicion_02_julio_26':
                        titulo = "Edición N.º 2 – Julio 2026"
                if titulo:
                    diario_item["titulo"] = titulo
                
                portada = metadata.get(name_lower, {}).get('portada')
                if portada:
                    diario_item["portada"] = portada
                
                diario_item["tomos"] = tomo_files
                diarios.append(diario_item)
    
    # Custom Sort: 'el guardian' 1st, 'edicion_02_julio_26' 2nd, 'el universo' 3rd, 'el observador' 4th, then rest alphabetically
    priority = {
        'el guardian': 0,
        'edicion_02_julio_26': 0.5,
        'el universo': 1,
        'el observador': 2,
        'el guardian ii': 1000  # Put it last
    }
    
    diarios.sort(key=lambda x: (priority.get(x['name'].lower(), 99), x['name'].lower()))
    
    return diarios

def scan_mas(base_path):
    # Load existing metadata (categories and portadas)
    metadata = {}
    mas_json_path = os.path.join(base_path, 'mas.json')
    if os.path.exists(mas_json_path):
        try:
            with open(mas_json_path, 'r', encoding='utf-8') as f:
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
            print(f"Warning: Error loading mas.json: {e}")

    mas_items = []
    mas_dir = os.path.join(base_path, 'mas')
    
    if not os.path.exists(mas_dir):
        return mas_items

    # Iterate through each folder in 'mas' (first level)
    for lvl1_name in sorted(os.listdir(mas_dir)):
        lvl1_path = os.path.join(mas_dir, lvl1_name)
        if not os.path.isdir(lvl1_path):
            continue
            
        # Check if this folder has files directly (e.g. mas/ilustraciones/1.png)
        lvl1_files = []
        for file_name in sorted(os.listdir(lvl1_path)):
            file_path = os.path.join(lvl1_path, file_name)
            if os.path.isfile(file_path) and file_name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                lvl1_files.append({
                    "name": file_name,
                    "path": f"mas/{lvl1_name}/{file_name}"
                })
        
        if lvl1_files:
            name_lower = lvl1_name.lower()
            item = {
                "name": lvl1_name,
            }
            
            # Default category to the level 1 folder name
            categoria = metadata.get(name_lower, {}).get('categoria')
            if not categoria:
                categoria = lvl1_name
            item["categoria"] = categoria
            
            portada = metadata.get(name_lower, {}).get('portada')
            if portada:
                item["portada"] = portada
            
            item["tomos"] = lvl1_files
            mas_items.append(item)
        else:
            # If no direct files, scan subfolders (second level, e.g. mas/interior_design/URBANA/)
            for lvl2_name in sorted(os.listdir(lvl1_path)):
                lvl2_path = os.path.join(lvl1_path, lvl2_name)
                if os.path.isdir(lvl2_path):
                    lvl2_files = []
                    for file_name in sorted(os.listdir(lvl2_path)):
                        file_path = os.path.join(lvl2_path, file_name)
                        if os.path.isfile(file_path) and file_name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                            lvl2_files.append({
                                "name": file_name,
                                "path": f"mas/{lvl1_name}/{lvl2_name}/{file_name}"
                            })
                    
                    if lvl2_files:
                        name_lower = lvl2_name.lower()
                        item = {
                            "name": lvl2_name,
                        }
                        
                        # Default category to the level 1 folder name
                        categoria = metadata.get(name_lower, {}).get('categoria')
                        if not categoria:
                            categoria = lvl1_name
                        item["categoria"] = categoria
                        
                        portada = metadata.get(name_lower, {}).get('portada')
                        if portada:
                            item["portada"] = portada
                        
                        item["tomos"] = lvl2_files
                        mas_items.append(item)
    
    mas_items.sort(key=lambda x: x['name'].lower())
    return mas_items

if __name__ == "__main__":
    # Use the directory where the script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Generate diarios.json
    diarios_data = scan_diarios(base_dir)
    with open(os.path.join(base_dir, 'diarios.json'), 'w', encoding='utf-8') as f:
        json.dump(diarios_data, f, indent=4, ensure_ascii=False)
    print(f"Generated diarios.json with {len(diarios_data)} diarios.")
    
    # Generate mas.json
    mas_data = scan_mas(base_dir)
    with open(os.path.join(base_dir, 'mas.json'), 'w', encoding='utf-8') as f:
        json.dump(mas_data, f, indent=4, ensure_ascii=False)
    print(f"Generated mas.json with {len(mas_data)} items.")

