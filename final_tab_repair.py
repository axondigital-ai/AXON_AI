import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
in_gestiune_tab = False

# Codul de ierarhizare pregătit pentru injectare
hierarchical_code = [
    "                # --- START EPC DRILL-DOWN V12.8 ---\n",
    "                st.info('📋 Gestiune Ierarhică: Click pe categorii pentru detalii.')\n",
    "                inv_docs = db.collection('axon_inventory').stream()\n",
    "                inv_data = [d.to_dict() for d in inv_docs]\n",
    "                import pandas as pd\n",
    "                if inv_data:\n",
    "                    df_inv = pd.DataFrame(inv_data)\n",
    "                    cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n",
    "                    for c in cats:\n",
    "                        c_df = df_inv[df_inv['Categorie'] == c] if 'Categorie' in df_inv.columns else pd.DataFrame()\n",
    "                        if not c_df.empty:\n",
    "                            with st.expander(f'📁 {c.upper()} ({len(c_df)} repere)'):\n",
    "                                # Afișăm tabelul filtrat\n",
    "                                cols = [col for col in ['Material', 'Cantitate', 'UM', 'Status'] if col in c_df.columns]\n",
    "                                st.table(c_df[cols].reset_index(drop=True))\n",
    "                else:\n",
    "                    st.warning('Nu sunt date în inventar.')\n",
    "                # --- END EPC DRILL-DOWN ---\n"
]

for i, line in enumerate(lines):
    new_lines.append(line)
    # Căutăm exact unde începe Tab-ul de Gestiune (care este al 3-lea tab, deci index 2)
    if "with tabs[2]:" in line:
        # Injectăm codul imediat după definirea tab-ului
        new_lines.extend(hierarchical_code)
        print("🎯 [TARGET FOUND]: Tab-ul de Gestiune a fost localizat și actualizat.")

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [FINISH]: Interfața a fost reconstruită. Repornește aplicația.")
