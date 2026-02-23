import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
in_tab_2 = False
block_injected = False

# Definim coloanele extinse pentru vizibilitate totală
cols_epc = ['Material', 'Cantitate_Planificata', 'Cantitate_Receptionata', 'Cantitate_Instalata', 'UM', 'Status']

for line in lines:
    # 1. Identificăm Tab-ul de Gestiune
    if "with tabs[2]:" in line:
        in_tab_2 = True
        new_lines.append(line)
        # Injectăm imediat noul bloc complet
        indent = " " * (len(line) - len(line.lstrip()) + 4)
        new_lines.append(f"{indent}# --- START AXON GESTIUNE TIER-1 V18 ---\n")
        new_lines.append(f"{indent}try:\n")
        new_lines.append(f"{indent}    import pandas as pd\n")
        new_lines.append(f"{indent}    from google.cloud import firestore\n")
        new_lines.append(f"{indent}    db_v18 = firestore.Client()\n")
        new_lines.append(f"{indent}    st.subheader('📊 CONTROL PROGRES EPC - ROGVAIV')\n")
        new_lines.append(f"{indent}    data = [d.to_dict() for d in db_v18.collection('axon_inventory').stream()]\n")
        new_lines.append(f"{indent}    if data:\n")
        new_lines.append(f"{indent}        df_v18 = pd.DataFrame(data)\n")
        new_lines.append(f"{indent}        cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(f"{indent}        for c in cats:\n")
        new_lines.append(f"{indent}            c_df = df_v18[df_v18['Categorie'] == c] if 'Categorie' in df_v18.columns else pd.DataFrame()\n")
        new_lines.append(f"{indent}            if not c_df.empty:\n")
        new_lines.append(f"{indent}                with st.expander(f'📁 {{c.upper()}} ({{len(c_df)}} repere)'):\n")
        new_lines.append(f"{indent}                    # Afișăm coloanele cerute pentru progres\n")
        new_lines.append(f"{indent}                    view_cols = [col for col in {cols_epc} if col in c_df.columns]\n")
        new_lines.append(f"{indent}                    st.dataframe(c_df[view_cols], use_container_width=True, hide_index=True)\n")
        new_lines.append(f"{indent}    else: st.warning('Inventar gol.')\n")
        new_lines.append(f"{indent}except Exception as e: st.error(f'Eroare: {{e}}')\n")
        new_lines.append(f"{indent}# --- END AXON GESTIUNE TIER-1 ---\n")
        block_injected = True
        continue

    # 2. Logica de ștergere a tabelului vechi ("FANTOMA")
    if in_tab_2:
        # Dacă linia conține comenzi de afișare tabel care NU sunt în blocul nostru, le ignorăm
        stripped = line.strip()
        if any(x in stripped for x in ["st.dataframe", "st.table", "st.write(df)", "st.write(inventory)"]):
            if "# ---" not in line: # Dacă nu e comentariul nostru, e tabelul vechi
                print(f"🗑️ Șters tabel redundant: {stripped}")
                continue
        
        # Dacă ieșim din indentarea tab-ului, oprim curățenia
        if line.strip() != "" and not line.startswith(" " * 8): # Ajustat pentru structura ta
            if "with" not in line and "tabs" not in line:
                in_tab_2 = False

    if not block_injected or not in_tab_2:
        new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [UPGRADE FINALIZAT]: Detaliile de progres au fost adăugate și tabelele vechi eliminate.")
