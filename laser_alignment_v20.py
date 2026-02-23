import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip_mode = False

for line in lines:
    # 1. Curățăm orice bloc de gestiune anterior pentru a evita duplicarea
    if "START AXON GESTIUNE" in line:
        skip_mode = True
        continue
    if "END AXON GESTIUNE" in line:
        skip_mode = False
        continue
    if skip_mode:
        continue

    new_lines.append(line)

    # 2. Identificăm punctul de ancorare și măsurăm indentarea
    if "with tabs[2]:" in line:
        # Calculăm câte spații are linia cu tab-ul
        base_indent = len(line) - len(line.lstrip())
        i1 = " " * (base_indent + 4)  # Nivelul 1 (try/except)
        i2 = i1 + "    "              # Nivelul 2 (codul interior)
        i3 = i2 + "    "              # Nivelul 3 (în interiorul 'if' sau 'for')

        # Injectăm blocul cu aliniere garantată
        new_lines.append(i1 + "# --- START AXON GESTIUNE V20.1 (ALINIAT) ---\n")
        new_lines.append(i1 + "try:\n")
        new_lines.append(i2 + "import pandas as pd\n")
        new_lines.append(i2 + "from google.cloud import firestore\n")
        new_lines.append(i2 + "db_v = firestore.Client()\n")
        new_lines.append(i2 + "st.subheader('📊 CONTROL EPC: SKU vs. PVCASE')\n")
        new_lines.append(i2 + "data_raw = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]\n")
        new_lines.append(i2 + "if data_raw:\n")
        new_lines.append(i3 + "df_v = pd.DataFrame(data_raw)\n")
        new_lines.append(i3 + "cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(i3 + "for c in cats:\n")
        new_lines.append(i3 + "    c_df = df_v[df_v['Categorie'] == c] if 'Categorie' in df_v.columns else pd.DataFrame()\n")
        new_lines.append(i3 + "    if not c_df.empty:\n")
        new_lines.append(i3 + "        with st.expander('📁 ' + c.upper() + ' (' + str(len(c_df)) + ')'):\n")
        new_lines.append(i3 + "            v_cols = ['Material', 'Cod_PVcase', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Status']\n")
        new_lines.append(i3 + "            actual_cols = [col for col in v_cols if col in c_df.columns]\n")
        new_lines.append(i3 + "            st.dataframe(c_df[actual_cols], use_container_width=True, hide_index=True)\n")
        new_lines.append(i1 + "except Exception as e:\n")
        new_lines.append(i2 + "st.error('Eroare vizualizare: ' + str(e))\n")
        new_lines.append(i1 + "# --- END AXON GESTIUNE V20.1 ---\n")

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [OPERATIUNE REUSITA]: Indentarea a fost calibrată laser sub tabs[2].")
