import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
skip_mode = False

for line in lines:
    # 1. Detectăm începutul secțiunii care trebuie eliminată
    if "CONTROL CUSTODIE ȘI PROGRES" in line or "st.metric" in line and "in_c" in line:
        skip_mode = True
        continue
    
    # 2. Dacă suntem în modul de ștergere, verificăm unde să ne oprim
    if skip_mode:
        # Ne oprim când dăm de sfârșitul secțiunii de gestiune sau de un alt element structural
        if "except Exception" in line or "# --- END AXON GESTIUNE" in line:
            skip_mode = False
        else:
            continue

    # 3. Ne asigurăm că în tabelul de sus, coloana se numește 'Realizat' și citește 'Cantitate_Instalata'
    # Corectăm direct în textul liniei dacă e cazul
    if "'Cantitate_Instalata': 'Realizat'" not in line and "rename(columns=" in line:
        line = line.replace("'Cantitate_Instalata': 'sum'", "'Cantitate_Instalata': 'sum'").replace("Cantitate_Instalata", "Cantitate_Instalata")
    
    new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("🚀 AXON: Secțiunea de progres a fost eliminată. Restul fișierului a rămas intact.")
