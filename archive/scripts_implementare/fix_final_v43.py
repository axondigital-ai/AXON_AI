import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False

for line in lines:
    if "with tabs[2]:" in line:
        new_lines.append(line)
        # Indentarea fixă: 16 spații pentru nivelul 1 sub 'with', 20 pentru nivelul 2
        indent_1 = " " * 16 + "    "
        indent_2 = indent_1 + "    "
        indent_3 = indent_2 + "    "
        
        new_lines.append(f"{indent_1}# --- START AXON GESTIUNE V43 ---\n")
        new_lines.append(f"{indent_1}try:\n")
        new_lines.append(f"{indent_2}import pandas as pd\n")
        new_lines.append(f"{indent_2}from google.cloud import firestore\n")
        new_lines.append(f"{indent_2}db_v = firestore.Client()\n")
        new_lines.append(f"{indent_2}data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]\n")
        
        new_lines.append(f"{indent_2}if data:\n")
        new_lines.append(f"{indent_3}df = pd.DataFrame(data)\n")
        new_lines.append(f"{indent_3}for col in ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Validata']:\n")
        new_lines.append(f"{indent_3}    if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)\n")
        
        new_lines.append(f"{indent_3}df['Mat_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0])\n")
        
        # TABELUL EPC (SUS)
        new_lines.append(f"{indent_3}st.subheader('📊 CONTROL OPERAȚIONAL EPC')\n")
        new_lines.append(f"{indent_3}summary = df.groupby(['Categorie', 'Mat_Baza']).agg({{'Cantitate_Planificata':'sum','Cantitate_Receptionata':'sum','Cantitate_Custodie':'sum','Cantitate_Validata':'sum'}}).reset_index()\n")
        new_lines.append(f"{indent_3}for cat in ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']:\n")
        new_lines.append(f"{indent_3}    c_df = summary[summary['Categorie'].str.strip() == cat].copy()\n")
        new_lines.append(f"{indent_3}    if not c_df.empty:\n")
        new_lines.append(f"{indent_3}        c_df['În Depozit'] = c_df['Cantitate_Receptionata'] - (c_df['Cantitate_Custodie'] + c_df['Cantitate_Validata'])\n")
        new_lines.append(f"{indent_3}        c_df = c_df.rename(columns={{'Cantitate_Planificata':'Planificat','Cantitate_Receptionata':'Total Intrat','Cantitate_Custodie':'În Custodie','Cantitate_Validata':'Realizat (PV)'}})\n")
        new_lines.append(f"{indent_3}        with st.expander(f'📁 {{cat.upper()}} ({{len(c_df)}})'):\n")
        new_lines.append(f"{indent_3}            st.dataframe(c_df[['Mat_Baza', 'Planificat', 'Total Intrat', 'În Depozit', 'În Custodie', 'Realizat (PV)']], use_container_width=True, hide_index=True)\n")
        
        # TABELUL CONTRACTORI (JOS) - REGULA GENERALĂ DE VIZIBILITATE
        new_lines.append(f"{indent_3}st.markdown('---')\n")
        new_lines.append(f"{indent_3}st.subheader('📈 SITUAȚIE CONTRACTORI (DETALIU CUSTODIE)')\n")
        # Afișăm orice rând care are legătură cu un contractor sau are stoc în teren
        new_lines.append(f"{indent_3}cust_df = df[(df['Material'].str.contains(r'\(', na=False)) | (df['Cantitate_Custodie'] > 0) | (df['Cantitate_Validata'] > 0)].copy()\n")
        new_lines.append(f"{indent_3}if not cust_df.empty:\n")
        new_lines.append(f"{indent_3}    cust_view = cust_df.rename(columns={{'Cantitate_Validata': 'Validat (PV)'}})\n")
        new_lines.append(f"{indent_3}    st.dataframe(cust_view[['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Validat (PV)', 'Status']], use_container_width=True, hide_index=True)\n")
        new_lines.append(f"{indent_3}else: st.info('ℹ️ Niciun material în custodie. Efectuați un handover.')\n")
        
        new_lines.append(f"{indent_1}except Exception as e: st.error(f'Eroare: {{e}}')\n")
        new_lines.append(f"{indent_1}# --- END AXON GESTIUNE ---\n")
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
print("✅ Indentarea a fost corectată manual. Aplicația este stabilă.")
