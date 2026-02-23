import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip_mode = False

# Blocul de cod corect indentat (folosim spații, nu tab-uri)
def get_clean_block(base_spaces):
    s4 = " " * (base_spaces + 4)
    s8 = " " * (base_spaces + 8)
    s12 = " " * (base_spaces + 12)
    return [
        f"{s4}# --- AXON GESTIUNE TIER-1 ---\n",
        f"{s4}try:\n",
        f"{s8}from google.cloud import firestore\n",
        f"{s8}import pandas as pd\n",
        f"{s8}db_l = firestore.Client()\n",
        f"{s8}st.markdown('### 📊 Gestiune Ierarhică EPC')\n",
        f"{s8}data = [d.to_dict() for d in db_l.collection('axon_inventory').stream()]\n",
        f"{s8}if data:\n",
        f"{s12}df_i = pd.DataFrame(data)\n",
        f"{s12}cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n",
        f"{s12}for c in cats:\n",
        f"{s12}    c_df = df_i[df_i['Categorie'] == c] if 'Categorie' in df_i.columns else pd.DataFrame()\n",
        f"{s12}    if not c_df.empty:\n",
        f"{s12}        with st.expander(f'📁 {{c.upper()}} ({{len(c_df)}})'):\n",
        f"{s12}            st.table(c_df[['Material', 'Cantitate', 'UM', 'Status']])\n",
        f"{s8}else:\n",
        f"{s12}st.warning('Bază de date goală.')\n",
        f"{s4}except Exception as e:\n",
        f"{s8}st.error(f'Eroare sistem: {{e}}')\n",
        f"{s4}# --- END AXON GESTIUNE ---\n"
    ]

for line in lines:
    # 1. Curățăm resturile de cod defect (ștergem liniile dintre START și END dacă există)
    if "--- START EPC" in line or "# --- START AXON GESTIUNE" in line:
        skip_mode = True
        continue
    if "--- END EPC" in line or "# --- END AXON GESTIUNE" in line:
        skip_mode = False
        continue
    if skip_mode:
        continue

    # 2. Păstrăm codul original, dar eliminăm manual liniile care au dat eroare anterior
    if "from google.cloud import firestore" in line or "db_local = firestore.Client()" in line:
        continue

    new_lines.append(line)

    # 3. Injectăm noul bloc exact sub Tab-ul de Gestiune
    if "with tabs[2]:" in line:
        base_indent = len(line) - len(line.lstrip())
        new_lines.extend(get_clean_block(base_indent))

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [OPERATIUNE REUSITA]: Codul a fost reconstruit de la zero cu indentare garantată.")
