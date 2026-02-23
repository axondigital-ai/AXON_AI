import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
patch_applied = False

# Blocul de cod complet independent
independent_code = [
    "                # --- START EPC SELF-HEALING V13.0 ---\n",
    "                try:\n",
    "                    from google.cloud import firestore\n",
    "                    import pandas as pd\n",
    "                    # Inițializăm un client local pentru a evita NameError\n",
    "                    db_local = firestore.Client()\n",
    "                    st.info('📊 Gestiune Proiect ROGVAIV - Control Total')\n",
    "                    \n",
    "                    inv_docs = db_local.collection('axon_inventory').stream()\n",
    "                    inv_data = [d.to_dict() for d in inv_docs]\n",
    "                    \n",
    "                    if inv_data:\n",
    "                        df_inv = pd.DataFrame(inv_data)\n",
    "                        cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n",
    "                        for c in cats:\n",
    "                            if 'Categorie' in df_inv.columns:\n",
    "                                c_df = df_inv[df_inv['Categorie'] == c]\n",
    "                                if not c_df.empty:\n",
    "                                    with st.expander(f'📁 {c.upper()} ({len(c_df)} repere)'):\n",
    "                                        cols = [col for col in ['Material', 'Cantitate', 'UM', 'Status'] if col in c_df.columns]\n",
    "                                        st.table(c_df[cols].reset_index(drop=True))\n",
    "                    else:\n",
    "                        st.warning('Inventarul este momentan gol în baza de date.')\n",
    "                except Exception as e:\n",
    "                    st.error(f'Eroare Gestiune: {e}')\n",
    "                # --- END EPC SELF-HEALING ---\n"
]

for line in lines:
    # Curățăm orice tentativă anterioară de patch (V12.8 sau V12.9)
    if "START EPC DRILL-DOWN" in line or "END EPC DRILL-DOWN" in line or "inv_docs = db.collection" in line:
        continue
    
    new_lines.append(line)
    
    # Căutăm linia cu Tab-ul de Gestiune
    if "with tabs[2]:" in line:
        leading_spaces = len(line) - len(line.lstrip())
        inner_indent = " " * (leading_spaces + 4)
        
        # Injectăm codul cu indentarea corectă
        for p_line in independent_code:
            new_lines.append(inner_indent + p_line.lstrip())
        patch_applied = True

if patch_applied:
    with open(file_path, "w") as f:
        f.writelines(new_lines)
    print("✅ [FIX APLICAT]: Gestiunea a fost izolată și reparată cu succes.")
else:
    print("❌ [EROARE]: Nu s-a putut localiza locul injecției.")
