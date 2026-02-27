import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_content = []
skip = False

for line in lines:
    if "with tabs[2]:" in line:
        new_content.append(line)
        indent = " " * 16
        i2 = indent + "    "
        i3 = i2 + "    "
        
        # Injectăm codul stabil
        new_content.append(i2 + "# --- START AXON GESTIUNE V38 --- \n")
        new_content.append(i2 + "try:\n")
        new_content.append(i3 + "import pandas as pd\n")
        new_content.append(i3 + "from google.cloud import firestore\n")
        new_content.append(i3 + "db_v = firestore.Client()\n")
        new_content.append(i3 + "data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]\n")
        new_content.append(i3 + "if data:\n")
        new_content.append(i3 + "    df = pd.DataFrame(data)\n")
        new_content.append(i3 + "    for c in ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Cantitate_Validata']:\n")
        new_content.append(i3 + "        if c in df.columns: df[c] = pd.to_numeric(df[col], errors='coerce').fillna(0) if 'col' in locals() else pd.to_numeric(df[c], errors='coerce').fillna(0)\n")
        
        # TABELUL EPC (SUS)
        new_content.append(i3 + "    st.subheader('📊 CONTROL OPERAȚIONAL EPC (DATE OFICIALE)')\n")
        new_content.append(i3 + "    df['Mat_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0])\n")
        new_content.append(i3 + "    sum_df = df.groupby(['Categorie', 'Mat_Baza']).agg({'Cantitate_Planificata':'sum','Cantitate_Receptionata':'sum','Cantitate_Custodie':'sum','Cantitate_Validata':'sum'}).reset_index()\n")
        
        new_content.append(i3 + "    for cat in ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']:\n")
        new_content.append(i3 + "        c_df = sum_df[sum_df['Categorie'].str.strip() == cat]\n")
        new_content.append(i3 + "        with st.expander(f'📁 {cat.upper()} ({len(c_df)})'):\n")
        new_content.append(i3 + "            if not c_df.empty:\n")
        new_content.append(i3 + "                v = c_df.rename(columns={'Cantitate_Custodie':'In Custodie','Cantitate_Validata':'Realizat (PV)'})\n")
        new_content.append(i3 + "                st.dataframe(v[['Mat_Baza', 'Cantitate_Planificata', 'Cantitate_Receptionata', 'In Custodie', 'Realizat (PV)']], use_container_width=True, hide_index=True)\n")
        
        # TABELUL DETALII (JOS)
        new_content.append(i3 + "    st.markdown('---')\n")
        new_content.append(i3 + "    st.subheader('📈 DETALII CONTRACTORI (SITUAȚIE TEREN)')\n")
        new_content.append(i3 + "    d_df = df[(df['Cantitate_Custodie']>0)|(df['Cantitate_Instalata']>0)|(df['Cantitate_Validata']>0)]\n")
        new_content.append(i3 + "    if not d_df.empty:\n")
        new_content.append(i3 + "        dv = d_df.rename(columns={'Cantitate_Instalata':'Raportat Constructor','Cantitate_Validata':'Validat PM'})\n")
        new_content.append(i3 + "        st.dataframe(dv[['Material','Contractor_Custodie','Cantitate_Custodie','Raportat Constructor','Validat PM','Status']], use_container_width=True, hide_index=True)\n")
        
        new_content.append(i2 + "except Exception as e: st.error(f'Eroare: {e}')\n")
        new_content.append(i2 + "# --- END AXON GESTIUNE --- \n")
        skip = True
        continue
    
    if skip:
        if "with tabs[" in line or "# --- END AXON GESTIUNE ---" in line:
            if "# --- END AXON GESTIUNE ---" in line: continue # Sare peste marcatorul vechi
            skip = False
        else:
            continue
            
    new_content.append(line)

with open(file_path, "w") as f:
    f.writelines(new_content)

print("✅ [V38.0]: Rescriere finalizată. Secțiunea Realizat (PV) forțată.")
