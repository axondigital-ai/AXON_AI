import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
patch_applied = False

for line in lines:
    # Eliminăm absolut orice urmă de tentative anterioare (V12.8, V12.9, V13.0)
    if any(x in line for x in ["START EPC", "END EPC", "Gestiune Ierarhică", "inv_docs =", "db_local =", "df_inv ="]):
        continue
    
    new_lines.append(line)
    
    # Căutăm linia cu Tab-ul de Gestiune (linia 214-215 la tine)
    if "with tabs[2]:" in line:
        # Detectăm indentarea de bază a tab-ului
        base_indent = " " * (len(line) - len(line.lstrip()))
        sub = base_indent + "    "     # Nivelul try
        sub2 = sub + "    "           # Nivelul interior try
        
        # Injectăm codul cu aliniere manuală forțată
        new_lines.append(f"{sub}# --- START EPC FINAL ALIGNMENT ---\n")
        new_lines.append(f"{sub}try:\n")
        new_lines.append(f"{sub2}from google.cloud import firestore\n")
        new_lines.append(f"{sub2}import pandas as pd\n")
        new_lines.append(f"{sub2}db_local = firestore.Client()\n")
        new_lines.append(f"{sub2}st.info('📊 GESTIUNE DETALIATĂ - PROIECT ROGVAIV')\n")
        new_lines.append(f"{sub2}docs = db_local.collection('axon_inventory').stream()\n")
        new_lines.append(f"{sub2}inv_data = [d.to_dict() for d in docs]\n")
        new_lines.append(f"{sub2}if inv_data:\n")
        new_lines.append(f"{sub2}    df_inv = pd.DataFrame(inv_data)\n")
        new_lines.append(f"{sub2}    cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(f"{sub2}    for c in cats:\n")
        new_lines.append(f"{sub2}        if 'Categorie' in df_inv.columns:\n")
        new_lines.append(f"{sub2}            c_df = df_inv[df_inv['Categorie'] == c]\n")
        new_lines.append(f"{sub2}            if not c_df.empty:\n")
        new_lines.append(f"{sub2}                with st.expander(f'📁 {{c.upper()}} ({{len(c_df)}} repere)'):\n")
        new_lines.append(f"{sub2}                    cols = [col for col in ['Material', 'Cantitate', 'UM', 'Status'] if col in c_df.columns]\n")
        new_lines.append(f"{sub2}                    st.table(c_df[cols].reset_index(drop=True))\n")
        new_lines.append(f"{sub}except Exception as e:\n")
        new_lines.append(f"{sub2}st.error(f'Eroare aliniere date: {{e}}')\n")
        new_lines.append(f"{sub}# --- END EPC FINAL ALIGNMENT ---\n")
        patch_applied = True

if patch_applied:
    with open(file_path, "w") as f:
        f.writelines(new_lines)
    print("✅ [FIX FINALIZAT]: Codul a fost aliniat corect. Eroarea de indentare a fost eliminată.")
else:
    print("❌ [EROARE]: Locația 'with tabs[2]' nu a fost găsită.")
