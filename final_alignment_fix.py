import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip_old_patch = False

for line in lines:
    # 1. Curățăm orice rest de la încercările anterioare (V12-V15)
    if any(tag in line for tag in ["START AXON", "END AXON", "START EPC", "END EPC", "Gestiune Ierarhică"]):
        skip_old_patch = True
        continue
    if skip_old_patch and ("# --- END" in line or "--- END" in line):
        skip_old_patch = False
        continue
    if skip_old_patch:
        continue

    # Eliminăm liniile orfane care au dat eroare
    if "try:" in line and "st.info" not in line and "tabs[2]" not in line:
        continue
    if "import pandas as pd" in line or "from google.cloud import firestore" in line:
        if "with tabs[2]" not in line: # Păstrăm doar dacă sunt în alt context (rar)
            continue

    new_lines.append(line)

    # 2. Injectăm blocul curat sub Tab-ul de Gestiune
    if "with tabs[2]:" in line:
        # Forțăm indentarea manuală (spații, nu tab-uri)
        # Dacă "with tabs[2]" este la coloana 12, try va fi la 16, restul la 20
        indent_base = " " * (len(line) - len(line.lstrip()))
        i1 = indent_base + "    " # Nivelul TRY
        i2 = i1 + "    "          # Nivelul COD INTERIOR
        
        new_lines.append(f"{i1}# --- AXON GESTIUNE STABILĂ V16 ---\n")
        new_lines.append(f"{i1}try:\n")
        new_lines.append(f"{i2}import pandas as pd\n")
        new_lines.append(f"{i2}from google.cloud import firestore\n")
        new_lines.append(f"{i2}db_v16 = firestore.Client()\n")
        new_lines.append(f"{i2}st.markdown('### 📊 Gestiune Detaliată')\n")
        new_lines.append(f"{i2}items = [d.to_dict() for d in db_v16.collection('axon_inventory').stream()]\n")
        new_lines.append(f"{i2}if items:\n")
        new_lines.append(f"{i2}    df_v16 = pd.DataFrame(items)\n")
        new_lines.append(f"{i2}    cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(f"{i2}    for c in cats:\n")
        new_lines.append(f"{i2}        if 'Categorie' in df_v16.columns:\n")
        new_lines.append(f"{i2}            c_df = df_v16[df_v16['Categorie'] == c]\n")
        new_lines.append(f"{i2}            if not c_df.empty:\n")
        new_lines.append(f"{i2}                with st.expander(f'📁 {{c.upper()}} ({{len(c_df)}})'):\n")
        new_lines.append(f"{i2}                    st.table(c_df[['Material', 'Cantitate', 'UM', 'Status']])\n")
        new_lines.append(f"{i1}except Exception as e:\n")
        new_lines.append(f"{i2}st.error(f'Eroare Gestiune: {{e}}')\n")
        new_lines.append(f"{i1}# --- END AXON GESTIUNE V16 ---\n")

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [FINISH]: Codul a fost reconstruit cu aliniere strictă.")
