import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False

for line in lines:
    if "START AXON GESTIUNE" in line:
        skip = True
        continue
    if "END AXON GESTIUNE" in line:
        skip = False
        continue
    
    if not skip:
        new_lines.append(line)
        
    if "with tabs[2]:" in line:
        i1 = " " * 20
        i2 = " " * 24
        i3 = " " * 28
        
        new_lines.append(i1 + "# --- START AXON GESTIUNE V28 (FIX SYNTAX) ---\n")
        new_lines.append(i1 + "try:\n")
        new_lines.append(i2 + "import pandas as pd\n")
        new_lines.append(i2 + "from google.cloud import firestore\n")
        new_lines.append(i2 + "db_v = firestore.Client()\n")
        new_lines.append(i2 + "data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]\n")
        
        new_lines.append(i2 + "if data:\n")
        new_lines.append(i3 + "df = pd.DataFrame(data)\n")
        new_lines.append(i3 + "for c in ['Cantitate_Planificata', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Cantitate_Receptionata']:\n")
        new_lines.append(i3 + "    if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)\n")
        
        # TABELUL DE SUS: TOTALURI EPC (Grupate pe Material)
        new_lines.append(i3 + "st.subheader('📊 CONTROL OPERAȚIONAL EPC (TOTALURI)')\n")
        new_lines.append(i3 + "df['Material_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0])\n")
        new_lines.append(i3 + "summary_df = df.groupby(['Material_Baza', 'Categorie']).agg({\n")
        new_lines.append(i3 + "    'Cantitate_Planificata': 'sum',\n")
        new_lines.append(i3 + "    'Cantitate_Receptionata': 'sum',\n")
        new_lines.append(i3 + "    'Cantitate_Custodie': 'sum',\n")
        new_lines.append(i3 + "    'Cantitate_Instalata': 'sum'\n")
        new_lines.append(i3 + "}).reset_index()\n")
        new_lines.append(i3 + "st.dataframe(summary_df, use_container_width=True, hide_index=True)\n")
        
        # TABELUL DE JOS: CUSTODIE ȘI PROGRES (Detaliat pe Contractori)
        new_lines.append(i3 + "st.markdown('---')\n")
        new_lines.append(i3 + "st.subheader('📈 DETALII CUSTODIE ȘI PROGRES CONTRACTORI')\n")
        new_lines.append(i3 + "custody_df = df[(df['Cantitate_Custodie'] > 0) | (df['Cantitate_Instalata'] > 0)]\n")
        new_lines.append(i3 + "if not custody_df.empty:\n")
        new_lines.append(i3 + "    cols_c = ['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Status']\n")
        new_lines.append(i3 + "    st.dataframe(custody_df[[c for c in cols_c if c in custody_df.columns]], use_container_width=True, hide_index=True)\n")
        
        # DASHBOARD METRICI - FIX SYNTAX AICI (folosim ghilimele duble la coloane)
        new_lines.append(i3 + "st.markdown('---')\n")
        new_lines.append(i3 + "c1, c2, c3 = st.columns(3)\n")
        new_lines.append(i3 + "c1.metric('Total Planificat (Unit)', f'{int(summary_df[\"Cantitate_Planificata\"].sum()):,}')\n")
        new_lines.append(i3 + "c2.metric('In Custodie', f'{int(summary_df[\"Cantitate_Custodie\"].sum()):,}')\n")
        new_lines.append(i3 + "c3.metric('Instalat', f'{int(summary_df[\"Cantitate_Instalata\"].sum()):,}')\n")

        new_lines.append(i1 + "except Exception as e: st.error('Eroare: ' + str(e))\n")
        new_lines.append(i1 + "# --- END AXON GESTIUNE V28 ---\n")

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [FIX V28]: SyntaxError rezolvat. Arhitectura Summary/Details a fost păstrată.")
