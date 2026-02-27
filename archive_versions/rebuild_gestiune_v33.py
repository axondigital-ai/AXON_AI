import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_content = []
in_gestiune_tab = False
done = False

for line in lines:
    if "with tabs[2]:" in line:
        new_content.append(line)
        # Injectăm codul curat direct aici
        indent = " " * 16
        i2 = indent + "    "
        i3 = i2 + "    "
        
        new_content.append(i2 + "# --- START AXON GESTIUNE V33 (FINAL CLEAN) ---\n")
        new_content.append(i2 + "try:\n")
        new_content.append(i3 + "import pandas as pd\n")
        new_content.append(i3 + "from google.cloud import firestore\n")
        new_content.append(i3 + "db_v = firestore.Client()\n")
        new_content.append(i3 + "data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]\n")
        new_content.append(i3 + "if data:\n")
        new_content.append(i3 + "    df = pd.DataFrame(data)\n")
        # Forțăm formatele numerice pentru calcule
        new_content.append(i3 + "    for col in ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Instalata']:\n")
        new_content.append(i3 + "        if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)\n")
        
        # TABELUL 1: TOTALURI EPC
        new_content.append(i3 + "    st.subheader('📊 CONTROL OPERAȚIONAL EPC')\n")
        new_content.append(i3 + "    df['Material_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0])\n")
        new_content.append(i3 + "    summ = df.groupby(['Categorie', 'Material_Baza']).agg({'Cantitate_Planificata':'sum','Cantitate_Receptionata':'sum','Cantitate_Custodie':'sum','Cantitate_Instalata':'sum'}).reset_index()\n")
        
        new_content.append(i3 + "    cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_content.append(i3 + "    for c in cats:\n")
        new_content.append(i3 + "        c_df = summ[summ['Categorie'].str.strip() == c]\n")
        new_content.append(i3 + "        with st.expander('📁 ' + c.upper() + ' (' + str(len(c_df)) + ')'):\n")
        new_content.append(i3 + "            if not c_df.empty:\n")
        new_content.append(i3 + "                view = c_df.rename(columns={'Cantitate_Instalata': 'Realizat'})\n")
        new_content.append(i3 + "                st.dataframe(view[['Material_Baza', 'Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Realizat']], use_container_width=True, hide_index=True)\n")
        
        # TABELUL 2: DETALII CONTRACTORI (DOAR ATÂT)
        new_content.append(i3 + "    st.markdown('---')\n")
        new_content.append(i3 + "    st.subheader('📈 DETALII CUSTODIE CONTRACTORI')\n")
        new_content.append(i3 + "    det_df = df[(df['Cantitate_Custodie'] > 0) | (df['Cantitate_Instalata'] > 0)]\n")
        new_content.append(i3 + "    if not det_df.empty:\n")
        new_content.append(i3 + "        det_view = det_df.rename(columns={'Cantitate_Instalata': 'Realizat'})\n")
        new_content.append(i3 + "        st.dataframe(det_view[['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Realizat', 'Status']], use_container_width=True, hide_index=True)\n")
        
        new_content.append(i2 + "except Exception as e: st.error(f'Eroare: {e}')\n")
        new_content.append(i2 + "# --- END AXON GESTIUNE ---\n")
        in_gestiune_tab = True
        continue

    # Această logică sare peste tot codul vechi până la următorul tab sau finalul secțiunii
    if in_gestiune_tab:
        if "with tabs[" in line or "# --- END AXON GESTIUNE ---" in line:
            in_gestiune_tab = False
            # Nu adăugăm linia curentă dacă e marcatorul de end, pentru că l-am adăugat deja mai sus
        else:
            continue

    new_content.append(line)

with open(file_path, "w") as f:
    f.writelines(new_content)

print("✅ [V33.0]: Reconstrucție completă. Secțiunile vechi eliminate fizic.")
