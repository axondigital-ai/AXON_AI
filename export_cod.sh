#!/bin/bash
OUTPUT_FILE="SITUATIE_AXON.txt"
echo "--- SITUATIE PROIECT AXON ---" > $OUTPUT_FILE
echo "Data export: $(date)" >> $OUTPUT_FILE
echo "---------------------------" >> $OUTPUT_FILE

# Adaugam structura directoarelor
echo -e "\n[STRUCTURA DOSARE]" >> $OUTPUT_FILE
tree -I 'venv|__pycache__|.git' >> $OUTPUT_FILE || ls -R -I venv -I __pycache__ >> $OUTPUT_FILE

# Extragem continutul fisierelor Python, Bash si SQL
echo -e "\n[CONTINUT COD]" >> $OUTPUT_FILE
find . -maxdepth 2 -not -path '*/.*' -type f \( -name "*.py" -o -name "*.sh" -o -name "*.sql" -o -name ".env" \) | while read file; do
    echo -e "\n\n--- FISIER: $file ---" >> $OUTPUT_FILE
    cat "$file" >> $OUTPUT_FILE
done

echo "Gata! Codul a fost extras in $OUTPUT_FILE"
