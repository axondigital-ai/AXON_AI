import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False

for line in lines:
    # 1. Curățăm orice tentativă anterioară (V19, V20, V21, V22)
    if "START AXON GESTIUNE" in line:
        skip = True
        continue
    if "END AXON GESTIUNE" in line:
        skip = False
        continue
    
    if not skip:
        new_lines.append(line)
        
    # 2. Injectăm blocul NOU imediat sub tab-ul 2 cu indentare fixă de 20 de spații
    if "with tabs[2]:" in line:
        # Indentarea standard: 16 spații pentru 'with', deci 20 pentru 'try'
        indent_1 = " " * 20
        indent_2 = " " * 24
        indent_3 = " " * 28
        
        new_lines.append(f"{indent_1}# --- START AXON GESTIUNE V23 (FINAL) ---\n")
        new_lines.append(f"{indent_1}try:\n")
        new_lines.append(f"{indent_2}import pandas as pd\n")
        new_lines.append(f"{indent_2}from google.cloud import firestore\n")
        new_lines.append(f"{indent_2}db_v = firestore.Client()\n")
        
        # DEFINIM 'data' AICI - UNIFICAT
        new_lines.append(f"{indent_2}docs = db_v.collection('axon_inventory').stream()\n")
        new_lines.append(f"{indent_2}data = [d.to_dict() for d in docs]\n")
        
        new_lines.append(f"{indent_2}if not data:\n")
        new_lines.append(f"{indent_3}st.warning('⚠️ Baza de date este goală.')\n")
        new_lines.append(f"{indent_2}else:\n")
        new_lines.append(f"{indent_3}df_v = pd.DataFrame(data)\n")
        new_lines.append(f"{indent_3}st.subheader('📊 CONTROL OPERAȚIONAL EPC')\n")
        
        # TABELE PE CATEGORII
        new_lines.append(f"{indent_3}cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(f"{indent_3}for c in cats:\n")
        new_lines.append(f"{indent_3}    c_df = df_v[df_v['Categorie'] == c] if 'Categorie' in df_v.columns else pd.DataFrame()\n")
        new_lines.append(f"{indent_3}    with st.expander('📁 ' + c.upper() + ' (' + str(len(c_df)) + ')'):\n")
        new_lines.append(f"{indent_3}        if not c_df.empty:\n")
        new_lines.append(f"{indent_3}            cols = ['Material', 'Cod_PVcase', 'Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Status']\n")
        new_lines.append(f"{indent_3}            st.dataframe(c_df[[col for col in cols if col in c_df.columns]], use_container_width=True, hide_index=True)\n")
        
        # DASHBOARD DE PROGRES (JOS)
        new_lines.append(f"{indent_3}st.markdown('---')\n")
        new_lines.append(f"{indent_3}st.subheader('📈 CONTROL CUSTODIE ȘI PROGRES')\n")
        new_lines.append(f"{indent_3}c1, c2, c3 = st.columns(3)\n")
        new_lines.append(f"{indent_3}in_c = df_v['Cantitate_Custodie'].sum() if 'Cantitate_Custodie' in df_v.columns else 0\n")
        new_lines.append(f"{indent_3}inst = df_v['Cantitate_Instalata'].sum() if 'Cantitate_Instalata' in df_v.columns else 0\n")
        new_lines.append(f"{indent_3}c1.metric('Repere', len(df_v))\n")
        new_lines.append(f"{indent_3}c2.metric('În Custodie', f'{int(in_c):,}')\n")
        new_lines.append(f"{indent_3}c3.metric('Instalat', f'{int(inst):,}')\n")
        
        new_lines.append(f"{indent_1}except Exception as e: st.error('Eroare Gestiune: ' + str(e))\n")
        new_lines.append(f"{indent_1}# --- END AXON GESTIUNE V23 (FINAL) ---\n")

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [FIX V23]: Indentare aliniată și variabila 'data' unificată.")
