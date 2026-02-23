import os
import shutil

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")
backup_path = file_path + ".backup_emergency"

# 1. Facem backup
shutil.copyfile(file_path, backup_path)
print(f"🛡️ Backup creat: {backup_path}")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False

# 2. Reconstruim fișierul linie cu linie
for line in lines:
    # Dacă găsim vechea încercare de patch sau tabelul vechi, îl înlocuim
    if "st.dataframe(df)" in line or "st.table(df)" in line or "LOGICĂ NOUĂ" in line:
        indent = line[:line.find(line.lstrip())] # Păstrăm indentarea originală
        new_lines.append(f"{indent}st.subheader('📊 Gestiune Proiect ROGVAIV - Ierarhie EPC')\n")
        new_lines.append(f"{indent}cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(f"{indent}for c in cats:\n")
        new_lines.append(f"{indent}    c_df = df[df['Categorie'] == c] if 'Categorie' in df.columns else df\n")
        new_lines.append(f"{indent}    if not c_df.empty:\n")
        new_lines.append(f"{indent}        with st.expander(f'📁 {{c.upper()}} ({{len(c_df)}} repere)'):\n")
        new_lines.append(f"{indent}            st.table(c_df[['Material', 'Cantitate', 'UM', 'Status']])\n")
    else:
        new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [FIX APLICAT]: Codul a fost curățat și ierarhia a fost forțată.")
