import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "with tabs[2]:" in line:
        new_lines.append(line)
        base_indent = " " * (len(line) - len(line.lstrip()) + 4)
        i2 = base_indent + "    "
        i3 = i2 + "    "
        i4 = i3 + "    "
        
        new_lines.append(f"{base_indent}try:\n")
        new_lines.append(f"{i2}import pandas as pd\n")
        new_lines.append(f"{i2}from google.cloud import firestore\n")
        new_lines.append(f"{i2}db_v = firestore.Client()\n")
        new_lines.append(f"{i2}data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]\n")
        
        new_lines.append(f"{i2}if data:\n")
        new_lines.append(f"{i3}df = pd.DataFrame(data)\n")
        new_lines.append(f"{i3}cols = ['Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Cantitate_Validata']\n")
        new_lines.append(f"{i3}for c in cols:\n")
        new_lines.append(f"{i4}if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)\n")
        
        new_lines.append(f"{i3}df['Mat_Baza'] = df['Material'].apply(lambda x: str(x).split(' (')[0].strip())\n")
        new_lines.append(f"{i3}df['Categorie'] = df['Categorie'].str.strip()\n")
        
        new_lines.append(f"{i3}st.subheader('📊 CONTROL OPERAȚIONAL EPC (PROGRES REAL)')\n")
        new_lines.append(f"{i3}summary = df.groupby(['Categorie', 'Mat_Baza']).agg({{'Cantitate_Planificata':'sum','Cantitate_Receptionata':'sum','Cantitate_Custodie':'sum','Cantitate_Validata':'sum'}}).reset_index()\n")
        
        new_lines.append(f"{i3}cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(f"{i3}for cat in cats:\n")
        new_lines.append(f"{i4}c_df = summary[summary['Categorie'] == cat].copy()\n")
        new_lines.append(f"{i4}with st.expander(f'📁 {{cat.upper()}} ({{len(c_df)}})'):\n")
        new_lines.append(f"{i4}    if not c_df.empty:\n")
        new_lines.append(f"{i4}        c_df['În Depozit'] = c_df['Cantitate_Receptionata'] - (c_df['Cantitate_Custodie'] + c_df['Cantitate_Validata'])\n")
        new_lines.append(f"{i4}        c_df['Progres Real'] = (c_df['Cantitate_Validata'] / c_df['Cantitate_Planificata']).fillna(0)\n")
        
        new_lines.append(f"{i4}        c_v = c_df.rename(columns={{'Mat_Baza':'Articol','Cantitate_Planificata':'Planificat','Cantitate_Receptionata':'Total Intrat','Cantitate_Custodie':'În Custodie','Cantitate_Validata':'Realizat (PV)'}})\n")
        new_lines.append(f"{i4}        display_df = c_v[['Articol', 'Planificat', 'Total Intrat', 'În Depozit', 'În Custodie', 'Realizat (PV)', 'Progres Real']]\n")
        
        # AICI E "ALTA PARTE": Folosim Styler-ul de Pandas pentru BARA VERDE și PROCENT
        new_lines.append(f"{i4}        styled_df = display_df.style.format({{'Progres Real': '{{:.1%}}'}})\\\n")
        new_lines.append(f"{i4}            .bar(subset=['Progres Real'], color='#28a745', vmin=0, vmax=1)\n")
        
        new_lines.append(f"{i4}        st.write(styled_df.to_html(escape=False, index=False), unsafe_allow_html=True)\n")
        
        new_lines.append(f"{i3}st.markdown('---')\n")
        new_lines.append(f"{i3}st.subheader('📈 SITUAȚIE CONTRACTORI (DETALIU CUSTODIE)')\n")
        new_lines.append(f"{i3}cust_df = df[df['Material'].str.contains(r'\(', na=False) | (df['Cantitate_Custodie'] > 0)].copy()\n")
        new_lines.append(f"{i3}if not cust_df.empty:\n")
        new_lines.append(f"{i3}    st.table(cust_df.rename(columns={{'Cantitate_Validata': 'Validat (PV)'}})[['Material', 'Contractor_Custodie', 'Cantitate_Custodie', 'Validat (PV)', 'Status']])\n")
        
        new_lines.append(f"{base_indent}except Exception as e: st.error(f'Eroare: {{e}}')\n")
        skip = True
        continue
    
    if skip and ("with tabs[" in line or "with st.sidebar" in line):
        skip = False
    if not skip:
        new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)
