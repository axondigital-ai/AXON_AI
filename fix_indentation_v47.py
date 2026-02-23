import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False

for line in lines:
    # Detectăm începutul tabului de Gestiune
    if "with tabs[2]:" in line:
        new_lines.append(line)
        # Nivelul 1 de indentare (sub with) - 16 spații (presupunând structura ta) + 4
        i1 = " " * 20 
        i2 = i1 + "    "
        i3 = i2 + "    "
        i4 = i3 + "    "
        
        # Injectăm codul cu indentare garantată
        new_lines.append(f"{i1}# --- START AXON GESTIUNE V47 ---\n")
        new_lines.append(f"{i1}try:\n")
        new_lines.append(f"{i2}import pandas as pd\n")
        new_lines.append(f"{i2}from google.cloud import firestore\n")
        new_lines.append(f"{i2}db_v = firestore.Client()\n")
        new_lines.append(f"{i2}docs = db_v.collection('axon_inventory').stream()\n")
        new_lines.append(f"{i2}data = [d.to_dict() for d in docs]\n")
        
        new_lines.append(f"{i2}if data:\n")
        new_lines.append(f"{i3}df = pd.DataFrame(data)\n")
        new_lines.append(f"{i3}num_cols = ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Validata']\n")
        new_lines.append(f"{i3}for c in num_cols:\n")
        new_lines.append(f"{i4}if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)\n")
        
        new_lines.append(f"{i3}df['Categorie'] = df['Categorie'].astype(str).str.strip()\n")
        new_lines.append(f"{i3}df['Mat_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0].strip())\n")
        
        # TABELUL EPC (SUS)
        new_lines.append(f"{i3}st.subheader('📊 CONTROL OPERAȚIONAL EPC')\n")
        new_lines.append(f"{i3}summary = df.groupby(['Categorie', 'Mat_Baza']).agg({{'Cantitate_Planificata':'sum','Cantitate_Receptionata':'sum','Cantitate_Custodie':'sum','Cantitate_Validata':'sum'}}).reset_index()\n")
        
        new_lines.append(f"{i3}cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(f"{i3}for cat in cats:\n")
        new_lines.append(f"{i4}c_df = summary[summary['Categorie'] == cat].copy()\n")
        new_lines.append(f"{i4}with st.expander(f'📁 {{cat.upper()}} ({{len(c_df)}})'):\n")
        new_lines.append(f"{i4}    if not c_df.empty:\n")
        new_lines.append(f"{i4}        c_df['În Depozit'] = c_df['Cantitate_Receptionata'] - (c_df['Cantitate_Custodie'] + c_df['Cantitate_Validata'])\n")
        new_lines.append(f"{i4}        c_view = c_df.rename(columns={{'Mat_Baza':'Articol','Cantitate_Planificata':'Planificat','Cantitate_Receptionata':'Total Intrat','Cantitate_Custodie':'În Custodie','Cantitate_Validata':'Realizat (PV)'}})\n")
        new_lines.append(f"{i4}        st.dataframe(c_view[['Articol', 'Planificat', 'Total Intrat', 'În Depozit', 'În Custodie', 'Realizat (PV)']], use_container_width=True, hide_index=True)\n")
        
        # TABELUL CONTRACTORI (JOS)
        new_lines.append(f"{i3}st.markdown('---')\n")
        new_lines.append(f"{i3}st.subheader('📈 SITUAȚIE CONTRACTORI (DETALIU CUSTODIE)')\n")
        new_lines.append(f"{i3}cust_df = df[df['Material'].str.contains(r'\(', na=False) | (df['Cantitate_Custodie'] > 0) | (df['Cantitate_Validata'] > 0)].copy()\n")
        new_lines.append(f"{i3}if not cust_df.empty:\n")
        new_lines.append(f"{i3}    st.dataframe(cust_df.rename(columns={{'Cantitate_Validata': 'Validat (PV)'}})[['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Validat (PV)', 'Status']], use_container_width=True, hide_index=True)\n")
        new_lines.append(f"{i3}else: st.info('ℹ️ Nu există materiale în custodie.')\n")
        
        new_lines.append(f"{i1}except Exception as e: st.error(f'Eroare Gestiune: {{e}}')\n")
        new_lines.append(f"{i1}# --- END AXON GESTIUNE ---\n")
        skip = True
        continue

    if skip:
        # Sărim peste liniile vechi până la următorul tab sau sfârșitul blocului
        if "with tabs[" in line or "# --- END AXON GESTIUNE ---" in line:
            if "# --- END AXON GESTIUNE ---" in line: continue
            skip = False
        else:
            continue
    new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [V47.0]: Indentare reparată. Regula de Aur și Categoriile sunt conservate.")
