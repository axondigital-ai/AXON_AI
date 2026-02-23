import os

file_path = os.path.expanduser("~/AXON_CORE/axon_core_os.py")

with open(file_path, "r") as f:
    lines = f.readlines()

new_lines = []
inside_gestiune_tab = False
hierarchical_finished = False

for line in lines:
    # Detectăm dacă suntem în Tab-ul de Gestiune
    if "with tabs[2]:" in line:
        inside_gestiune_tab = True
        new_lines.append(line)
        continue

    # Detectăm sfârșitul blocului nostru ierarhic
    if "# --- END AXON GESTIUNE" in line or "# --- END EPC" in line:
        hierarchical_finished = True
        new_lines.append(line)
        continue

    # Dacă am terminat desenul ierarhic, dar încă suntem în același Tab,
    # ignorăm liniile care încearcă să mai afișeze tabele (df sau inventory)
    if inside_gestiune_tab and hierarchical_finished:
        stripped = line.strip()
        if stripped.startswith("st.dataframe") or stripped.startswith("st.table") or stripped.startswith("st.write(df)"):
            print(f"🗑️ Eliminat tabel redundant: {stripped}")
            continue
        
        # Dacă dăm de un alt "with" sau o linie neindentată, înseamnă că am ieșit din tab
        if line.lstrip() == line and line.strip() != "":
            inside_gestiune_tab = False
            hierarchical_finished = False

    new_lines.append(line)

with open(file_path, "w") as f:
    f.writelines(new_lines)

print("✅ [CLEANUP REUȘIT]: Tabelul vechi a fost eliminat. A rămas doar vizualizarea pe categorii.")
