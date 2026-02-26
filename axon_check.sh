#!/bin/bash

# 1. Configurare URL Sitemark Mock
MOCK_URL="https://774a211a-8af7-46de-a0a7-f20587872219.mock.pstmn.io/progress"

# 2. Datele raportate de Contractor (Ground Truth)
declare -A contractor_val=( ["STS-01"]=45 ["STS-02"]=100 ["STS-05"]=100 )

echo "🛰️ AXON CORE: Pornire sincronizare aeriană..."

# 3. Preluăm datele
response=$(curl -s "$MOCK_URL")

# Verificăm dacă răspunsul este valid (nu e null)
check_null=$(echo "$response" | jq '.sts_units')

if [ "$check_null" == "null" ] || [ -z "$response" ]; then
    echo "❌ EROARE CRITICĂ: Datele de la dronă sunt NULL."
    echo "👉 Verifică în Postman: 1. Apasă SAVE pe Example. 2. URL-ul trebuie să se termine în /progress"
    exit 1
fi

# 4. Afișare Tabel
printf "\n%-10s | %-12s | %-8s | %-15s\n" "UNITATE" "CONTRACTOR" "DRONĂ" "STATUS VALIDARE"
echo "------------------------------------------------------------"

echo "$response" | jq -c '.sts_units[]' | while read -r unit; do
    id=$(echo "$unit" | jq -r '.id')
    drone_val=$(echo "$unit" | jq -r '.panels')
    cont_val=${contractor_val[$id]}
    
    if [ ! -z "$cont_val" ]; then
        diff=$((cont_val - drone_val))
        if [ "$diff" -eq 0 ]; then status="✅ Validat"; elif [ "$diff" -le 5 ]; then status="⚠️ Discrepanta"; else status="🛑 BLOCAT PLATA"; fi
        printf "%-10s | %-11d%% | %-7d%% | %-15s\n" "$id" "$cont_val" "$drone_val" "$status"
    fi
done

echo -e "\n[VERIFICAT AXON] Sincronizare finalizată la $(date)"
