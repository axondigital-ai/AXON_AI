import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def hard_reset():
    print("\n⚡ AXON CORE: Resetarea conștiinței Managerului General...")
    
    # 🛡️ SAFE SCRIPTING: Suprascriem documentul pentru a elimina zgomotul vechi
    pm_ref = db.collection("axon_protocols").document("Project_Manager")
    
    clean_dna = {
        "identitate": "MASTER PROJECT MANAGER - ROGVAIV 350MWp",
        "versiune_logica": "12.6_HIERARCHICAL",
        "instructiune_principala": "Gestiunea este organizată IERARHIC pe 5 CATEGORII. Nu raporta detalii mărunte decât la cerere.",
        "structura_master": {
            "CAT_1": "Major Assets (Panouri, Invertoare, STS)",
            "CAT_2": "Mechanical (Trackers, Piloni, Cleme)",
            "CAT_3": "DC Electrical (Cabluri, Conectori)",
            "CAT_4": "AC & Earthing (MT, Împământare, Papuci)",
            "CAT_5": "Consumables (Coliere, Tuburi, Vopsea Torque)"
        },
        "regula_de_audit": "Verifică întotdeauna dacă pentru cele 6.820 trackere avem înregistrate 2.046.000 de cleme în baza de date.",
        "mod_vizualizare": "Nivel 1 (Categorii) -> Nivel 2 (Componente Principale) -> Nivel 3 (Marunțișuri)"
    }
    
    pm_ref.set(clean_dna) # FĂRĂ merge=True pentru a curăța tot ce era vechi
    print("✅ [SUCCESS]: Managerul General a fost reinițializat.")

if __name__ == "__main__":
    hard_reset()
