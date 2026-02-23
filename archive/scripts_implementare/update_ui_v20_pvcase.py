import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False

# Adăugăm Cod_PVcase în lista de coloane vizibile
cols_v20 = ['Material', 'Cod_PVcase', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Status']

for line in lines:
    if "START AXON GESTIUNE" in line:
        skip = True
        continue
    if "END AXON GESTIUNE" in line:
        skip = False
        indent = " " * (len(line) - len(line.lstrip()) - 4) # Păstrăm alinierea
        if indent == "": indent = " " * 16
        s = indent + "    "
        
        new_lines.append(f"{indent}# --- START AXON GESTIUNE V20 (PVCASE) ---\n")
        new_lines.append(f"{indent}try:\n")
        new_lines.append(f"{s}import pandas as pd\n")
        new_lines.append(f"{s}from google.cloud import firestore\n")
        new_lines.append(f"{s}db_v = firestore.Client()\n")
        new_lines.append(f"{s}st.subheader('📊 CONTROL EPC: SKU vs. PVCASE')\n")
        new_lines.append(f"{s}data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]\n")
        new_lines.append(f"{s}if data:\n")
        new_lines.append(f"{s}    df_v = pd.DataFrame(data)\n")
        new_lines.append(f"{s}    cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(f"{s}    for c in cats:\n")
        new_lines.append(f"{s}        c_df = df_v[df_v['Categorie'] == c] if 'Categorie' in df_v.columns else pd.DataFrame()\n")
        new_lines.append(f"{s}        if not c_df.empty:\n")
        new_lines.append(f"{s}            with st.expander('📁 ' + c.upper() + ' (' + str(len(c_df)) + ')'):\n")
        new_lines.append(f"{s}                v_cols = [col for col in {cols_v20} if col in c_df.columns]\n")
        new_lines.append(f"{s}                st.dataframe(c_df[v_cols], use_container_width=True, hide_index=True)\n")
        new_lines.append(f"{indent}except Exception as e: st.error('Eroare: ' + str(e))\n")
        new_lines.append(f"{indent}# --- END AXON GESTIUNE V20 ---\n")
        continue
    
    if not skip:
        new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [UI V20]: Coloana PVcase a fost adăugată în interfață.")
