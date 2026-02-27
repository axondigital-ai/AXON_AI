import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def hard_reset_pm():
    print("\n⚡ AXON AI: Executare HARD RESET pe DNA-ul Managerului General...")
    
    # Suprascriem complet documentul, fara merge=True, pentru a sterge instructiunile vechi
    new_dna = {
        "rol": "MANAGER GENERAL (MASTER AGENT) - AXON CORE OS",
        "misiune_critica": "Supravegherea totala a Proiectului ROGVAIV (350.24 MWp)",
        "instructiuni_prioritare": [
            "1. RECONOASTE IERARHIA: Gestiunea nu mai are 7 linii, ci este structurata pe 5 CATEGORII MASTER (Major Assets, Mechanical, DC Electrical, AC, Consumables).",
            "2. ACCES TOTAL: Ai vizibilitate asupra celor 13+ repere detaliate, inclusiv cele 2.046.000 de cleme si 770.000 coliere.",
            "3. DRILL-DOWN: Raporteaza intai Executiv (Nivel 1), dar la orice intrebare despre stoc, verifica obligatoriu Nivelul 2 (Detaliu).",
            "4. AUDIT: Nu accepta rapoarte de progres daca materialele marunte (papuci, conectori, vopsea torque) nu sunt in stoc."
        ],
        "sursa_adevar": "Colectia Firestore: axon_inventory",
        "status": "ACTIVE_V12_HIERARCHY",
        "last_refresh": "2026-02-22"
    }
    
    # 🛡️ SAFE SCRIPTING: Setam fara merge pentru a curata contextul vechi
    db.collection("axon_protocols").document("Project_Manager").set(new_dna)
    
    print("✅ [RESTART COMPLET]: DNA-ul a fost curățat și actualizat.")
    print("💡 Managerul General este acum obligat să vadă Gestiunea de Detaliu.")

if __name__ == "__main__":
    hard_reset_pm()
