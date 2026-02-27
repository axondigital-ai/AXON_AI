#!/bin/bash
OUTPUT_FILE="$HOME/AXON_CORE/programator_activ.txt"

echo "=== SNAPSHOT SISTEM AXON CORE OS ===" > $OUTPUT_FILE
date >> $OUTPUT_FILE

echo -e "\n=== 1. STRUCTURA DIRECTORULUI ===" >> $OUTPUT_FILE
ls -lh $HOME/AXON_CORE | grep -v "venv\|archive_versions\|__pycache__" >> $OUTPUT_FILE

echo -e "\n=== 2. CONFIGURĂRI HARD/SOFT (.txt, .conf) ===" >> $OUTPUT_FILE
find $HOME/AXON_CORE -maxdepth 1 \( -name "*.txt" -o -name "*.conf" \) -not -name "programator_activ.txt" | while read fname; do
    echo -e "\n--- CONȚINUT: $(basename $fname) ---" >> $OUTPUT_FILE
    cat "$fname" >> $OUTPUT_FILE
done

echo -e "\n=== 3. SCHEMA BAZĂ DE DATE POSTGRESQL (axon_rogvaiv) ===" >> $OUTPUT_FILE
# Extragem doar structura (fără date) pentru a vedea cum arată tabelul gis_coordinates și axon_trackers
PGPASSWORD="Axon2026X" pg_dump -h 127.0.0.1 -U admin_axon -s axon_rogvaiv 2>/dev/null >> $OUTPUT_FILE || echo "Nu s-a putut extrage schema DB." >> $OUTPUT_FILE

echo -e "\n=== 4. COD SURSĂ PRINCIPAL (axon_core_os.py) ===" >> $OUTPUT_FILE
cat $HOME/AXON_CORE/axon_core_os.py >> $OUTPUT_FILE

echo "✅ Snapshot complet! Fișierul a fost generat."
