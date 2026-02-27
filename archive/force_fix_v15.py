import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False

for line in lines:
    # Eliminăm resturile de la încercările anterioare pentru a curăța fișierul
    if any(tag in line for tag in ["START EPC", "END EPC", "AXON GESTIUNE", "import pandas", "db_l =", "db_local ="]):
        continue
    
    new_lines.append(line)
    
    # Căutăm punctul de injecție (Tab-ul de Gestiune)
    if "with tabs[2]:" in line:
        # Calculăm indentarea de bază (câte spații are linia cu tab-ul)
        spaces = " " * (len(line) - len(line.lstrip()))
        s4 = spaces + "    "  # Primul nivel (try)
        s8 = s4 + "    "      # Al doilea nivel (codul din try)
        
        # Injectăm codul cu indentare manuală strictă
        new_lines.append(f"{s4}# --- START AXON CORE V15 ---\n")
        new_lines.append(f"{s4}try:\n")
        new_lines.append(f"{s8}import pandas as pd\n")
        new_lines.append(f"{s8}from google.cloud import firestore\n")
        new_lines.append(f"{s8}db_v15 = firestore.Client()\n")
        new_lines.append(f"{s8}st.markdown('### 📊 Gestiune Proiect ROGVAIV')\n")
        new_lines.append(f"{s8}inv_docs = db_v15.collection('axon_inventory').stream()\n")
        new_lines.append(f"{s8}inv_list = [d.to_dict() for d in inv_docs]\n")
        new_lines.append(f"{s8}if inv_list:\n")
        new_lines.append(f"{s8}    df_v15 = pd.DataFrame(inv_list)\n")
        new_lines.append(f"{s8}    cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        new_lines.append(f"{s8}    for c in cats:\n")
        new_lines.append(f"{s8}        if 'Categorie' in df_v15.columns:\n")
        new_lines.append(f"{s8}            c_df = df_v15[df_v15['Categorie'] == c]\n")
        new_lines.append(f"{s8}            if not c_df.empty:\n")
        new_lines.append(f"{s8}                with st.expander(f'📁 {{c.upper()}} ({{len(c_df)}} repere)'):\n")
        new_lines.append(f"{s8}                    st.table(c_df[['Material', 'Cantitate', 'UM', 'Status']])\n")
        new_lines.append(f"{s4}except Exception as e:\n")
        new_lines.append(f"{s8}st.error(f'Eroate Gestiune: {{e}}')\n")
        new_lines.append(f"{s4}# --- END AXON CORE V15 ---\n")

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [OPERATIUNE FINALIZATĂ]: Codul a fost aliniat forțat. Nu ar mai trebui să existe IndentationError.")
