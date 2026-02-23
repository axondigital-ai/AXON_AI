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
        # Indentare standard sub tabs[2]
        indent = " " * 16 
        s = indent + "    "
        s2 = s + "    "
        
        new_lines.append(indent + "# --- START AXON GESTIUNE V22.0 (UNIFICAT) ---\n")
        new_lines.append(indent + "try:\n")
        new_lines.append(s + "import pandas as pd\n")
        new_lines.append(s + "from google.cloud import firestore\n")
        new_lines.append(s + "db_v = firestore.Client()\n")
        
        # DEFINIM 'data' GLOBAL PENTRU TOT TABUL
        new_lines.append(s + "docs = db_v.collection('axon_inventory').stream()\n")
        new_lines.append(s + "data = [d.to_dict() for d in docs]\n")
        
        new_lines.append(s + "if not data:\n")
        new_lines.append(s2 + "st.warning('⚠️ Baza de date este goală. Rulați importul BOM.')\n")
        new_lines.append(s + "else:\n")
        new_lines.append(s2 + "df_v = pd.DataFrame(data)\n")
        new_lines.append(s2 + "st.subheader('📊 CONTROL OPERAȚIONAL EPC')\n")
        
        # 1. TABELELE PE CATEGORII
        new_lines.append(s2 + "cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(s2 + "for c in cats:\n")
        new_lines.append(s2 + "    c_df = df_v[df_v['Categorie'] == c] if 'Categorie' in df_v.columns else pd.DataFrame()\n")
        new_lines.append(s2 + "    with st.expander('📁 ' + c.upper() + ' (' + str(len(c_df)) + ')'):\n")
        new_lines.append(s2 + "        if not c_df.empty:\n")
        new_lines.append(s2 + "            cols = ['Material', 'Cod_PVcase', 'Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Status']\n")
        new_lines.append(s2 + "            st.dataframe(c_df[[col for col in cols if col in c_df.columns]], use_container_width=True, hide_index=True)\n")
        
        # 2. SECȚIUNEA DE JOS: CONTROL CUSTODIE ȘI PROGRES
        new_lines.append(s2 + "st.markdown('---')\n")
        new_lines.append(s2 + "st.subheader('📈 CONTROL CUSTODIE ȘI PROGRES FIZIC')\n")
        new_lines.append(s2 + "col1, col2, col3 = st.columns(3)\n")
        
        # Calculăm metricile din variabila 'data' care acum este definită sigur
        new_lines.append(s2 + "total_mat = len(df_v)\n")
        new_lines.append(s2 + "in_custodie = df_v['Cantitate_Custodie'].sum() if 'Cantitate_Custodie' in df_v.columns else 0\n")
        new_lines.append(s2 + "instalat = df_v['Cantitate_Instalata'].sum() if 'Cantitate_Instalata' in df_v.columns else 0\n")
        
        new_lines.append(s2 + "col1.metric('Repere Totale', total_mat)\n")
        new_lines.append(s2 + "col2.metric('În Custodie (Șantier)', f'{int(in_custodie):,}')\n")
        new_lines.append(s2 + "col3.metric('Progres Instalare', f'{int(instalat):,}')\n")
        
        # Bara de progres generală
        new_lines.append(s2 + "prog_proc = (instalat / df_v['Cantitate_Planificata'].sum()) if df_v['Cantitate_Planificata'].sum() > 0 else 0\n")
        new_lines.append(s2 + "st.progress(min(float(prog_proc), 1.0))\n")
        new_lines.append(s2 + "st.caption(f'Grad de finalizare proiect (bazat pe unități instalate): {prog_proc:.2%}')\n")

        new_lines.append(indent + "except Exception as e: st.error('Eroare Dashboard: ' + str(e))\n")
        new_lines.append(indent + "# --- END AXON GESTIUNE V22.0 ---\n")
        continue
    
    if not skip:
        new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [FIX V22.0]: Variabila 'data' a fost unificată. Dashboard-ul de progres este activ.")
