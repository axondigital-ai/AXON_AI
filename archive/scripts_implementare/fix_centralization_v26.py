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
        
        new_lines.append(i1 + "# --- START AXON GESTIUNE V26 (CENTRALIZAT) ---\n")
        new_lines.append(i1 + "try:\n")
        new_lines.append(i2 + "import pandas as pd\n")
        new_lines.append(i2 + "from google.cloud import firestore\n")
        new_lines.append(i2 + "db_v = firestore.Client()\n")
        new_lines.append(i2 + "data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]\n")
        
        new_lines.append(i2 + "if not data:\n")
        new_lines.append(i3 + "st.warning('Baza de date este goala.')\n")
        new_lines.append(i2 + "else:\n")
        new_lines.append(i3 + "df_v = pd.DataFrame(data)\n")
        
        # LOGICA DE CALCUL ROBUSTA (Centralizarea)
        new_lines.append(i3 + "for col in ['Cantitate_Custodie', 'Cantitate_Instalata', 'Cantitate_Planificata']:\n")
        new_lines.append(i3 + "    if col in df_v.columns: df_v[col] = pd.to_numeric(df_v[col], errors='coerce').fillna(0)\n")
        
        new_lines.append(i3 + "st.subheader('📊 CONTROL OPERAȚIONAL EPC')\n")
        new_lines.append(i3 + "cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(i3 + "for c in cats:\n")
        new_lines.append(i3 + "    c_df = df_v[df_v['Categorie'].str.strip() == c] if 'Categorie' in df_v.columns else pd.DataFrame()\n")
        new_lines.append(i3 + "    with st.expander('📁 ' + c.upper() + ' (' + str(len(c_df)) + ')'):\n")
        new_lines.append(i3 + "        if not c_df.empty:\n")
        new_lines.append(i3 + "            cols = ['Material', 'Cod_PVcase', 'Cantitate_Planificata', 'Cantitate_Custodie', 'Cantitate_Instalata', 'Status']\n")
        new_lines.append(i3 + "            st.dataframe(c_df[[col for col in cols if col in c_df.columns]], use_container_width=True, hide_index=True)\n")
        
        # DASHBOARD CENTRALIZAT (Fix NameError & Sum)
        new_lines.append(i3 + "st.markdown('---')\n")
        new_lines.append(i3 + "st.subheader('📈 CONTROL CUSTODIE ȘI PROGRES FIZIC')\n")
        new_lines.append(i3 + "c1, c2, c3 = st.columns(3)\n")
        
        new_lines.append(i3 + "total_plan = df_v['Cantitate_Planificata'].sum()\n")
        new_lines.append(i3 + "total_cust = df_v['Cantitate_Custodie'].sum()\n")
        new_lines.append(i3 + "total_inst = df_v['Cantitate_Instalata'].sum()\n")
        
        new_lines.append(i3 + "c1.metric('Repere Proiect', len(df_v))\n")
        new_lines.append(i3 + "c2.metric('In Custodie (Total)', f'{int(total_cust):,}')\n")
        new_lines.append(i3 + "c3.metric('Instalat (Total)', f'{int(total_inst):,}')\n")
        
        # BARA DE PROGRES REALA
        new_lines.append(i3 + "prog = (total_inst / total_plan) if total_plan > 0 else 0\n")
        new_lines.append(i3 + "st.progress(min(float(prog), 1.0))\n")
        new_lines.append(i3 + "st.write(f'**PROGRES GENERAL MODUL 01: {prog:.2%}**')\n")

        new_lines.append(i1 + "except Exception as e: st.error('Eroare Gestiune: ' + str(e))\n")
        new_lines.append(i1 + "# --- END AXON GESTIUNE V26 ---\n")

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [FIX V26]: Centralizarea a fost reparata prin conversie numerica forțată.")
