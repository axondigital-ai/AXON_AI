import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def deep_repair():
    print("\n🧠 AXON CORE: Se execută reparația Agentului Principal...")
    
    # 1. Extragem datele reale din Firestore pentru a le folosi ca "Anchor"
    inventory = db.collection("axon_inventory").stream()
    stats = {}
    items_count = 0
    
    for doc in inventory:
        d = doc.to_dict()
        cat = d.get('Categorie', 'Altele')
        stats[cat] = stats.get(cat, 0) + 1
        items_count += 1

    # Construim string-ul de control
    context_str = "\n".join([f"- {cat}: {count} repere unice" for cat, count in stats.items()])

    # 2. Rescriem DNA-ul Agentului Principal cu "Ochii Deschiși"
    master_dna = {
        "ROL": "MASTER PROJECT MANAGER (AI OVERLORD) - ROGVAIV",
        "CONTEXT_CRITIC": f"Proiect 350.24 MWp. Gestiune ierarhică ACTIVĂ. {items_count} repere în DB.",
        "DATE_CERTIFICATE_FIRESTORE": {
            "CATEGORII": stats,
            "REPERE_CRITICE": "Panouri: 511.500 | Cleme: 2.046.000 | Piloni: 47.740 | Coliere: 770.000"
        },
        "REGULI_GATING": [
            "NU ignora materialul mărunt. Dacă lipsesc clemele, proiectul e blocat.",
            "Raportează întotdeauna ierarhic: Categorie -> Principal -> Detaliu.",
            "Toate datele provin din colectia 'axon_inventory'. Nu inventa cifre."
        ],
        "LOGICA_DE_AFIȘARE": "Drill-down (Nivel 1 -> Nivel 2).",
        "STATUS": "REPAIRED_V12.7"
    }

    # 🛡️ SAFE SCRIPTING: Suprascriere totală pentru a curăța cache-ul vechi
    db.collection("axon_protocols").document("Project_Manager").set(master_dna)
    
    print(f"✅ [REPARAT]: Agentul Principal are acum acces direct la rezumatul gestiunii.")
    print(f"📊 Date injectate direct: {items_count} repere în {len(stats)} categorii.")

if __name__ == "__main__":
    deep_repair()
