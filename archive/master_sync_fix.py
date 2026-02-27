import os
import google.cloud.firestore as firestore

# 1. REPARAȚIE FIRESTORE (PROJECT_MANAGER CONTENT)
os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def clean_pm_content():
    pm_ref = db.collection("axon_protocols").document("Project_Manager")
    doc = pm_ref.get()
    if doc.exists:
        data = doc.to_dict()
        content = data.get("content", "")
        # Dacă conținutul e "murdar" cu format de dicționar, îl curățăm
        if "DATE_CERTIFICATE_FIRESTORE" in content:
            new_content = "PROTOCOL MASTER PROJECT MANAGER\n"
            new_content += "Statut: REPAIRED_V12.7\n"
            new_content += "Instrucțiuni: Gestionează proiectul ROGVAIV 350MWp folosind datele din axon_inventory.\n"
            new_content += "Configurație detectată: Ierarhie EPC activă pe 5 categorii."
            pm_ref.update({"content": new_content})
            print("✅ Firestore: Conținutul Project_Manager a fost sanitizat.")

# 2. REPARAȚIE COD (AXON_CORE_OS.PY)
file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

def fix_python_indentation():
    with open(file_path, "r") as f:
        lines = f.readlines()
    
    new_lines = []
    in_gestiune_tab = False
    
    for line in lines:
        # Eliminăm orice resturi de try/except care au cauzat eroarea la linia 216
        if any(tag in line for tag in ["START AXON GESTIUNE", "END AXON GESTIUNE", "db_v19"]):
            continue
        if "try:" in line and "import pandas" in "".join(lines[lines.index(line):lines.index(line)+5]):
            continue
            
        new_lines.append(line)
        
        # Injectăm blocul corect indentat sub Tab-ul 2
        if "with tabs[2]:" in line:
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            sub_indent = indent + "    "
            new_lines.append(f"{indent}# --- START AXON GESTIUNE V19.2 ---\n")
            new_lines.append(f"{indent}try:\n")
            new_lines.append(f"{sub_indent}import pandas as pd\n")
            new_lines.append(f"{sub_indent}from google.cloud import firestore\n")
            new_lines.append(f"{sub_indent}db_v = firestore.Client()\n")
            new_lines.append(f"{sub_indent}st.subheader('📊 CONTROL CUSTODIE ȘI PROGRES EPC')\n")
            new_lines.append(f"{sub_indent}inv_data = [d.to_dict() for d in db_v.collection('axon_inventory').stream()]\n")
            new_lines.append(f"{sub_indent}if inv_data:\n")
            new_lines.append(f"{sub_indent}    df_v = pd.DataFrame(inv_data)\n")
            new_lines.append(f"{sub_indent}    cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
            new_lines.append(f"{sub_indent}    for c in cats:\n")
            new_lines.append(f"{sub_indent}        c_df = df_v[df_v['Categorie'] == c] if 'Categorie' in df_v.columns else pd.DataFrame()\n")
            new_lines.append(f"{sub_indent}        if not c_df.empty:\n")
            new_lines.append(f"{sub_indent}            with st.expander(f'📁 {c.upper()} ({len(c_df)})'):\n")
            new_lines.append(f"{sub_indent}                cols = ['Material', 'Cantitate_Receptionata', 'Cantitate_Custodie', 'Contractor_Custodie', 'Cantitate_Instalata', 'Status']\n")
            new_lines.append(f"{sub_indent}                st.dataframe(c_df[[col for col in cols if col in c_df.columns]], use_container_width=True, hide_index=True)\n")
            new_lines.append(f"{indent}except Exception as e:\n")
            new_lines.append(f"{sub_indent}st.error(f'Eroare Gestiune: {e}')\n")
            new_lines.append(f"{indent}# --- END AXON GESTIUNE V19.2 ---\n")

    with open(file_path, "w") as f:
        f.writelines(new_lines)
    print("✅ Cod: Indentarea a fost aliniată forțat sub tabs[2].")

if __name__ == "__main__":
    clean_pm_content()
    fix_python_indentation()
