import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip = False

# Blocul de cod pentru Gestiunea Ierarhică
def get_gestiune_ui(base_indent):
    i1 = " " * (base_indent + 4)
    i2 = i1 + "    "
    i3 = i2 + "    "
    return [
        f"{i1}st.markdown('### 📊 GESTIUNE IERARHICĂ EPC - PROIECT ROGVAIV')\n",
        f"{i1}try:\n",
        f"{i2}import pandas as pd\n",
        f"{i2}from google.cloud import firestore\n",
        f"{i2}db_ui = firestore.Client()\n",
        f"{i2}data = [d.to_dict() for d in db_ui.collection('axon_inventory').stream()]\n",
        f"{i2}if data:\n",
        f"{i3}df_ui = pd.DataFrame(data)\n",
        f"{i3}cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n",
        f"{i3}for c in cats:\n",
        f"{i3}    c_df = df_ui[df_ui['Categorie'] == c] if 'Categorie' in df_ui.columns else pd.DataFrame()\n",
        f"{i3}    if not c_df.empty:\n",
        f"{i3}        with st.expander(f'📁 {{c.upper()}} ({{len(c_df)}} repere)'):\n",
        f"{i3}            st.table(c_df[['Material', 'Cantitate', 'UM', 'Status']])\n",
        f"{i2}else:\n",
        f"{i3}st.warning('Nu s-au găsit date în inventar.')\n",
        f"{i1}except Exception as e:\n",
        f"{i2}st.error(f'Eroare vizualizare: {{e}}')\n"
    ]

for line in lines:
    # Curățăm orice tentativă eșuată anterioară
    if "START EPC" in line or "END EPC" in line or "AXON GESTIUNE" in line or "try:" in line and "import pandas" in next((l for l in lines[lines.index(line):lines.index(line)+5]), ""):
        continue
    
    new_lines.append(line)
    
    # Căutăm exact locul unde se definește Tab-ul de Gestiune (tabs[2])
    if "with tabs[2]:" in line:
        indent = len(line) - len(line.lstrip())
        new_lines.extend(get_gestiune_ui(indent))

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [UI RECONSTRUIT]: Rubrica Gestiune a fost actualizată la formatul ierarhic.")
