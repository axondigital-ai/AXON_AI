import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

clean_lines = []
for line in lines:
    # Pasul 1: Convertim orice Tab în 4 spații pentru a evita IndentationError
    processed_line = line.replace('\t', '    ')
    
    # Pasul 2: Curățăm resturile de cod defect (V12-V16) care pot cauza conflicte
    if any(tag in processed_line for tag in ["START AXON", "END AXON", "START EPC", "END EPC", "AXON GESTIUNE"]):
        continue
    
    clean_lines.append(processed_line)

# Pasul 3: Fix special pentru linia 19 (Except orfan)
# Căutăm orice 'except:' care nu este aliniat și îl forțăm sub 'try'
final_lines = []
for i, line in enumerate(clean_lines):
    if "except:" in line and "return None" in line:
        # Forțăm indentarea standard pentru o funcție de top
        final_lines.append("    except: return None\n")
    else:
        final_lines.append(line)

# Pasul 4: Re-injectăm Gestiunea corect, o singură dată
updated_lines = []
for line in final_lines:
    updated_lines.append(line)
    if "with tabs[2]:" in line:
        indent = " " * (len(line) - len(line.lstrip()) + 4)
        updated_lines.append(f"{indent}try:\n")
        updated_lines.append(f"{indent}    import pandas as pd\n")
        updated_lines.append(f"{indent}    from google.cloud import firestore\n")
        updated_lines.append(f"{indent}    db_l = firestore.Client()\n")
        updated_lines.append(f"{indent}    st.markdown('### 📊 Gestiune Proiect ROGVAIV')\n")
        updated_lines.append(f"{indent}    inv = [d.to_dict() for d in db_l.collection('axon_inventory').stream()]\n")
        updated_lines.append(f"{indent}    if inv:\n")
        updated_lines.append(f"{indent}        df_i = pd.DataFrame(inv)\n")
        updated_lines.append(f"{indent}        cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']\n")
        updated_lines.append(f"{indent}        for c in cats:\n")
        updated_lines.append(f"{indent}            if 'Categorie' in df_i.columns:\n")
        updated_lines.append(f"{indent}                c_df = df_i[df_i['Categorie'] == c]\n")
        updated_lines.append(f"{indent}                if not c_df.empty:\n")
        updated_lines.append(f"{indent}                    with st.expander(f'📁 {{c.upper()}} ({{len(c_df)}})'):\n")
        updated_lines.append(f"{indent}                        st.table(c_df[['Material', 'Cantitate', 'UM', 'Status']])\n")
        updated_lines.append(f"{indent}except Exception as e:\n")
        updated_lines.append(f"{indent}    st.error(f'Eroare: {{e}}')\n")

with open(file_path, "w") as f:
    f.writelines(updated_lines)

print("✅ [RECONSTRUCȚIE COMPLETĂ]: Toate tab-urile au fost convertite în spații.")
print("🛠️ Linia 19 a fost aliniată forțat. Încearcă să pornești aplicația.")
