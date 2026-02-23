import os
import google.cloud.firestore as firestore

# 1. CURĂȚARE FIRESTORE
os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def clean_pm():
    ref = db.collection("axon_protocols").document("Project_Manager")
    ref.update({"content": "PROTOCOL MASTER PM V12.7\nStatut: ACTIV\nManagement ROGVAIV 350MWp."})
    print("✅ Firestore actualizat.")

# 2. REPARAȚIE COD .PY
file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

def fix_code():
    with open(file_path, "r") as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # Ștergem orice tentativă eșuată anterioară (V19.x)
        if any(x in line for x in ["START AXON GESTIUNE", "END AXON GESTIUNE", "db_v", "df_v"]):
            continue
        new_lines.append(line)
        
        # Injectăm codul corect sub tab-ul 2
        if "with tabs[2]:" in line:
            # Calculăm indentarea (4 spații sub 'with')
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            s = indent + "    "
            new_lines.append(indent + "# --- START AXON GESTIUNE V19.4 ---\n")
            new_lines.append(indent + "try:\n")
            new_lines.append(s + "import pandas as pd\n")
            new_lines.append(s + "from google.cloud import firestore\n")
            new_lines.append(s + "db_v = firestore.Client()\n")
            new_lines.append(s + "st.subheader('📊 CONTROL CUSTODIE ȘI PROGRES EPC')\n")
            new_lines.append(s + "inv_raw = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]\n")
            new_lines.append(s + "if inv_raw:\n")
            new_lines.append(s + "    df_v = pd.DataFrame(inv_raw)\n")
            new_lines.append(s + "    cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
            new_lines.append(s + "    for c in cats:\n")
            new_lines.append(s + "        c_df = df_v[df_v['Categorie'] == c] if 'Categorie' in df_v.columns else pd.DataFrame()\n")
            new_lines.append(s + "        if not c_df.empty:\n")
            # Folosim scriere directă pentru a evita erorile de tip NameError
            line_expander = s + "            with st.expander('📁 ' + c.upper() + ' (' + str(len(c_df)) + ')'):\n"
            new_lines.append(line_expander)
            new_lines.append(s + "                cols = ['Material', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Contractor_Custodie', 'Cantitate_Instalata', 'Status']\n")
            new_lines.append(s + "                st.dataframe(c_df[[col for col in cols if col in c_df.columns]], use_container_width=True, hide_index=True)\n")
            new_lines.append(indent + "except Exception as e:\n")
            new_lines.append(s + "st.error('Eroare Gestiune: ' + str(e))\n")
            new_lines.append(indent + "# --- END AXON GESTIUNE V19.4 ---\n")

    with open(file_path, "w") as f:
        f.writelines(new_lines)
    print("✅ Cod corectat și aliniat (v19.4).")

if __name__ == "__main__":
    clean_pm()
    fix_code()
