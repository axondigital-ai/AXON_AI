import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
patch_applied = False

for line in lines:
    # Păstrăm liniile originale, dar eliminăm orice tentativă eșuată de patch anterior
    if "--- START EPC DRILL-DOWN" in line or "Gestiune Ierarhică" in line:
        continue
    
    new_lines.append(line)
    
    # Căutăm linia cu Tab-ul de Gestiune
    if "with tabs[2]:" in line:
        # Detectăm automat câte spații sunt în fața liniei "with tabs[2]:"
        leading_spaces = len(line) - len(line.lstrip())
        inner_indent = " " * (leading_spaces + 4) # Adăugăm exact un nivel de indentare
        
        # Injectăm codul cu indentarea calculată matematic
        new_lines.append(f"{inner_indent}# --- START EPC DRILL-DOWN V12.9 ---\n")
        new_lines.append(f"{inner_indent}st.info('📋 Gestiune Ierarhică: Click pe categorii pentru detalii.')\n")
        new_lines.append(f"{inner_indent}inv_docs = db.collection('axon_inventory').stream()\n")
        new_lines.append(f"{inner_indent}inv_data = [d.to_dict() for d in inv_docs]\n")
        new_lines.append(f"{inner_indent}import pandas as pd\n")
        new_lines.append(f"{inner_indent}if inv_data:\n")
        new_lines.append(f"{inner_indent}    df_inv = pd.DataFrame(inv_data)\n")
        new_lines.append(f"{inner_indent}    cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(f"{inner_indent}    for c in cats:\n")
        new_lines.append(f"{inner_indent}        if 'Categorie' in df_inv.columns:\n")
        new_lines.append(f"{inner_indent}            c_df = df_inv[df_inv['Categorie'] == c]\n")
        new_lines.append(f"{inner_indent}            if not c_df.empty:\n")
        new_lines.append(f"{inner_indent}                with st.expander(f'📁 {{c.upper()}} ({{len(c_df)}} repere)'):\n")
        new_lines.append(f"{inner_indent}                    cols = [col for col in ['Material', 'Cantitate', 'UM', 'Status'] if col in c_df.columns]\n")
        new_lines.append(f"{inner_indent}                    st.table(c_df[cols].reset_index(drop=True))\n")
        new_lines.append(f"{inner_indent}# --- END EPC DRILL-DOWN ---\n")
        patch_applied = True

if patch_applied:
    with open(file_path, "w") as f:
        f.writelines(new_lines)
    print("✅ [FIX REUȘIT]: Indentarea a fost corectată automat conform structurii fișierului.")
else:
    print("❌ [EROARE]: Nu am găsit linia 'with tabs[2]:'. Verifică dacă agentul Procurement este activ.")

