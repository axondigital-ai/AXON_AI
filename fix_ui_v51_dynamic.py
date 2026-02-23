import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False

for line in lines:
    if "with tabs[2]:" in line:
        new_lines.append(line)
        base_indent = len(line) - len(line.lstrip())
        i1 = " " * (base_indent + 4)
        i2 = i1 + "    "
        i3 = i2 + "    "
        i4 = i3 + "    "
        
        new_lines.append(f"{i1}# --- AXON GESTIUNE V51 (DINAMICĂ TOTALĂ) ---\n")
        new_lines.append(f"{i1}try:\n")
        new_lines.append(f"{i2}import pandas as pd\n")
        new_lines.append(f"{i2}from google.cloud import firestore\n")
        new_lines.append(f"{i2}db_v = firestore.Client()\n")
        # CITIRE LIVE DIN DATABASE
        new_lines.append(f"{i2}data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]\n")
        new_lines.append(f"{i2}if data:\n")
        new_lines.append(f"{i3}df = pd.DataFrame(data)\n")
        new_lines.append(f"{i3}cols = ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Validata']\n")
        new_lines.append(f"{i3}for c in cols:\n")
        new_lines.append(f"{i4}if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)\n")
        
        new_lines.append(f"{i3}df['Categorie'] = df['Categorie'].astype(str).str.strip()\n")
        new_lines.append(f"{i3}df['Mat_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0].strip())\n")
        
        new_lines.append(f"{i3}st.subheader('📊 CONTROL OPERAȚIONAL EPC (PROGRES)')\n")
        new_lines.append(f"{i3}summary = df.groupby(['Categorie', 'Mat_Baza']).agg({{'Cantitate_Planificata':'sum','Cantitate_Receptionata':'sum','Cantitate_Custodie':'sum','Cantitate_Validata':'sum'}}).reset_index()\n")
        
        new_lines.append(f"{i3}cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(f"{i3}for cat in cats:\n")
        new_lines.append(f"{i4}c_df = summary[summary['Categorie'] == cat].copy()\n")
        new_lines.append(f"{i4}with st.expander(f'📁 {{cat.upper()}} ({{len(c_df)}})'):\n")
        new_lines.append(f"{i4}    if not c_df.empty:\n")
        new_lines.append(f"{i4}        # LOGICA DINAMICĂ: Fără date injectate\n")
        new_lines.append(f"{i4}        c_df['În Depozit'] = c_df['Cantitate_Receptionata'] - (c_df['Cantitate_Custodie'] + c_df['Cantitate_Validata'])\n")
        new_lines.append(f"{i4}        c_df['% Progres'] = c_df.apply(lambda r: r['Cantitate_Validata']/r['Cantitate_Planificata'] if r['Cantitate_Planificata'] > 0 else 0, axis=1)\n")
        new_lines.append(f"{i4}        c_v = c_df.rename(columns={{'Mat_Baza':'Articol','Cantitate_Planificata':'Planificat','Cantitate_Receptionata':'Total Intrat','Cantitate_Custodie':'În Custodie','Cantitate_Validata':'Realizat (PV)'}})\n")
        new_lines.append(f"{i4}        st.dataframe(c_v[['Articol', 'Planificat', 'Total Intrat', 'În Depozit', 'În Custodie', 'Realizat (PV)', '% Progres']], use_container_width=True, hide_index=True, column_config={{'% Progres': st.column_config.ProgressColumn('Status', format='%.1f%%', min_value=0, max_value=1)}})\n")
        
        new_lines.append(f"{i3}st.markdown('---')\n")
        new_lines.append(f"{i3}st.subheader('📈 SITUAȚIE CONTRACTORI (DETALIU CUSTODIE)')\n")
        new_lines.append(f"{i3}cust_df = df[df['Material'].str.contains(r'\(', na=False) | (df['Cantitate_Custodie'] > 0)].copy()\n")
        new_lines.append(f"{i3}if not cust_df.empty:\n")
        new_lines.append(f"{i3}    st.dataframe(cust_df.rename(columns={{'Cantitate_Validata': 'Validat (PV)'}})[['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Validat (PV)', 'Status']], use_container_width=True, hide_index=True)\n")
        
        new_lines.append(f"{i1}except Exception as e: st.error(f'Eroare Gestiune: {{e}}')\n")
        new_lines.append(f"{i1}# --- END AXON GESTIUNE ---\n")
        skip = True
        continue
    if skip:
        if "with tabs[" in line or "# --- END AXON GESTIUNE ---" in line:
            if "# --- END AXON GESTIUNE ---" in line: continue
            skip = False
        else: continue
    new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)
