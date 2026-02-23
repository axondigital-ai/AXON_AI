import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False

# Definim noile coloane care includ Custodia
cols_custody = ['Material', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Contractor_Custodie', 'Cantitate_Instalata', 'Status']

for line in lines:
    if "START AXON GESTIUNE" in line:
        skip = True
        continue
    if "END AXON GESTIUNE" in line:
        skip = False
        # Injectăm noua versiune v19
        indent = " " * 16 # Indentare standard pentru tab
        new_lines.append(f"{indent}# --- START AXON GESTIUNE V19 (CUSTODIE) ---\n")
        new_lines.append(f"{indent}try:\n")
        new_lines.append(f"{indent}    import pandas as pd\n")
        new_lines.append(f"{indent}    from google.cloud import firestore\n")
        new_lines.append(f"{indent}    db_v19 = firestore.Client()\n")
        new_lines.append(f"{indent}    st.subheader('📊 CONTROL CUSTODIE ȘI PROGRES')\n")
        new_lines.append(f"{indent}    data = [d.to_dict() for d in db_v19.collection('axon_inventory').stream()]\n")
        new_lines.append(f"{indent}    if data:\n")
        new_lines.append(f"{indent}        df_v19 = pd.DataFrame(data)\n")
        new_lines.append(f"{indent}        cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(f"{indent}        for c in cats:\n")
        new_lines.append(f"{indent}            c_df = df_v19[df_v19['Categorie'] == c] if 'Categorie' in df_v19.columns else pd.DataFrame()\n")
        new_lines.append(f"{indent}            if not c_df.empty:\n")
        new_lines.append(f"{indent}                with st.expander(f'📁 {{c.upper()}} ({{len(c_df)}})'):\n")
        new_lines.append(f"{indent}                    view_cols = [col for col in {cols_custody} if col in c_df.columns]\n")
        new_lines.append(f"{indent}                    st.dataframe(c_df[view_cols], use_container_width=True, hide_index=True)\n")
        new_lines.append(f"{indent}except Exception as e: st.error(f'Eroare: {{e}}')\n")
        new_lines.append(f"{indent}# --- END AXON GESTIUNE V19 ---\n")
        continue
    
    if not skip:
        new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [UI V19]: Vizualizarea Custodiei a fost activată.")
