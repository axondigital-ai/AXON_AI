import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
indent = ""

for line in lines:
    if "with tabs[2]:" in line:
        new_lines.append(line)
        # Calculăm indentarea actuală a liniei 'with' pentru a păstra alinierea
        indent = line[:line.find("with")]
        inner_indent = indent + "    " # 4 spații în plus
        
        # Injectăm codul cu indentarea corectă
        new_lines.append(f"{inner_indent}# --- START AXON GESTIUNE V40 (LOGICĂ REPARATĂ) ---\n")
        new_lines.append(f"{inner_indent}try:\n")
        i2 = inner_indent + "    "
        i3 = i2 + "    "
        
        new_lines.append(f"{i2}import pandas as pd\n")
        new_lines.append(f"{i2}from google.cloud import firestore\n")
        new_lines.append(f"{i2}db_v = firestore.Client()\n")
        new_lines.append(f"{i2}data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]\n")
        new_lines.append(f"{i2}if data:\n")
        new_lines.append(f"{i3}df = pd.DataFrame(data)\n")
        new_lines.append(f"{i3}for col in ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Cantitate_Validata']:\n")
        new_lines.append(f"{i3}    if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)\n")
        
        new_lines.append(f"{i3}df['Mat_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0])\n")
        new_lines.append(f"{i3}summary = df.groupby(['Categorie', 'Mat_Baza']).agg({{'Cantitate_Planificata': 'sum', 'Cantitate_Receptionata': 'sum', 'Cantitate_Custodie': 'sum', 'Cantitate_Validata': 'sum'}}).reset_index()\n")
        
        new_lines.append(f"{i2}st.subheader('📊 CONTROL OPERAȚIONAL EPC (STOCURI ȘI PROGRES)')\n")
        new_lines.append(f"{i2}cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(f"{i2}for c in cats:\n")
        new_lines.append(f"{i3}c_df = summary[summary['Categorie'].str.strip() == c].copy()\n")
        new_lines.append(f"{i3}if not c_df.empty:\n")
        new_lines.append(f"{i3}    c_df['În Depozit'] = c_df['Cantitate_Receptionata'] - (c_df['Cantitate_Custodie'] + c_df['Cantitate_Validata'])\n")
        new_lines.append(f"{i3}    c_df = c_df.rename(columns={{'Cantitate_Planificata': 'Planificat', 'Cantitate_Receptionata': 'Total Intrat', 'Cantitate_Custodie': 'În Custodie', 'Cantitate_Validata': 'Realizat (PV)'}})\n")
        new_lines.append(f"{i3}    with st.expander(f'📁 {{c.upper()}} ({{len(c_df)}})'):\n")
        new_lines.append(f"{i3}        st.dataframe(c_df[['Mat_Baza', 'Planificat', 'Total Intrat', 'În Depozit', 'În Custodie', 'Realizat (PV)']], use_container_width=True, hide_index=True)\n")
        
        new_lines.append(f"{i2}st.markdown('---')\n")
        new_lines.append(f"{i2}st.subheader('📈 SITUAȚIE CONTRACTORI (DETALIU CUSTODIE)')\n")
        new_lines.append(f"{i2}cust_df = df[(df['Cantitate_Custodie'] > 0) | (df['Cantitate_Instalata'] > 0) | (df['Cantitate_Validata'] > 0)].copy()\n")
        new_lines.append(f"{i2}if not cust_df.empty:\n")
        new_lines.append(f"{i2}    st.dataframe(cust_df[['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Cantitate_Validata', 'Status']], use_container_width=True, hide_index=True)\n")
        
        new_lines.append(f"{inner_indent}except Exception as e: st.error(f'Eroare Gestiune: {{e}}')\n")
        new_lines.append(f"{inner_indent}# --- END AXON GESTIUNE ---\n")
        skip = True
        continue

    if skip:
        if "with tabs[" in line or "# --- END AXON GESTIUNE ---" in line:
            if "# --- END AXON GESTIUNE ---" in line: continue
            skip = False
        else:
            continue
    new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)
print("✅ [V40.0]: Indentarea a fost corectată. Aplicația ar trebui să pornească acum.")
