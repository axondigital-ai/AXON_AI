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
        
        new_lines.append(i1 + "# --- START AXON GESTIUNE V29 (CLEAN & RESTORE) ---\n")
        new_lines.append(i1 + "try:\n")
        new_lines.append(i2 + "import pandas as pd\n")
        new_lines.append(i2 + "from google.cloud import firestore\n")
        new_lines.append(i2 + "db_v = firestore.Client()\n")
        new_lines.append(i2 + "data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]\n")
        
        new_lines.append(i2 + "if data:\n")
        new_lines.append(i3 + "df = pd.DataFrame(data)\n")
        # Conversie numerică sigură pentru toate calculele
        new_lines.append(i3 + "for c in ['Cantitate_Planificata', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Cantitate_Receptionata']:\n")
        new_lines.append(i3 + "    if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)\n")
        
        # TABELUL 1: CONTROL OPERAȚIONAL EPC (GRUPAT PE CATEGORII)
        new_lines.append(i3 + "st.subheader('📊 CONTROL OPERAȚIONAL EPC')\n")
        new_lines.append(i3 + "df['Material_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0])\n")
        
        # Grupăm datele pentru a avea totaluri pe material de bază
        new_lines.append(i3 + "summ = df.groupby(['Categorie', 'Material_Baza']).agg({\n")
        new_lines.append(i3 + "    'Cantitate_Planificata': 'sum', 'Cantitate_Receptionata': 'sum', \n")
        new_lines.append(i3 + "    'Cantitate_Custodie': 'sum', 'Cantitate_Instalata': 'sum'\n")
        new_lines.append(i3 + "}).reset_index()\n")
        
        new_lines.append(i3 + "cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(i3 + "for c in cats:\n")
        new_lines.append(i3 + "    c_df = summ[summ['Categorie'].str.strip() == c]\n")
        new_lines.append(i3 + "    with st.expander('📁 ' + c.upper() + ' (' + str(len(c_df)) + ')'):\n")
        new_lines.append(i3 + "        if not c_df.empty:\n")
        new_lines.append(i3 + "            st.dataframe(c_df, use_container_width=True, hide_index=True)\n")
        
        # TABELUL 2: DETALII CUSTODIE ȘI PROGRES (DOAR CONTRACTORI)
        new_lines.append(i3 + "st.markdown('---')\n")
        new_lines.append(i3 + "st.subheader('📈 DETALII CUSTODIE CONTRACTORI')\n")
        new_lines.append(i3 + "cust_df = df[(df['Cantitate_Custodie'] > 0) | (df['Cantitate_Instalata'] > 0)]\n")
        new_lines.append(i3 + "if not cust_df.empty:\n")
        new_lines.append(i3 + "    display_cols = ['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Status']\n")
        new_lines.append(i3 + "    st.dataframe(cust_df[[col for col in display_cols if col in cust_df.columns]], use_container_width=True, hide_index=True)\n")
        new_lines.append(i3 + "else: st.info('Nu există materiale în custodia contractorilor.')\n")

        new_lines.append(i1 + "except Exception as e: st.error('Eroare: ' + str(e))\n")
        new_lines.append(i1 + "# --- END AXON GESTIUNE V29 ---\n")

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [V29.0]: Organizarea pe categorii restaurată. Dashboard-ul problematic a fost eliminat.")
