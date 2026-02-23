import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def flash_sync():
    print("\n⚡ AXON CORE: Injectare Memorie de Context pentru Managerul General...")
    
    # 1. Colectăm statisticile reale din baza de date pentru a le pune direct în DNA
    inv_docs = db.collection("axon_inventory").stream()
    summary = {}
    total_items = 0
    
    for doc in inv_docs:
        d = doc.to_dict()
        cat = d.get('Categorie', 'Altele')
        summary[cat] = summary.get(cat, 0) + 1
        total_items += 1

    stats_str = ", ".join([f"{cat}: {count} repere" for cat, count in summary.items()])

    # 2. Scriem noul DNA cu datele deja pre-procesate
    pm_dna = {
        "status_activare": "FULL_AWARENESS",
        "context_proiect": "ROGVAIV 350.24 MWp",
        "arhitectura_stoc": f"IERARHICA (5 Categorii Master). Total repere detectate: {total_items}. Distributie: {stats_str}",
        "regula_imperativa": "Orice raspuns despre materiale TREBUIE sa inceapa cu verificarea colectiei 'axon_inventory'.",
        "detalii_critice": "Recunoaste cele 2.046.000 cleme, 770.000 coliere si restul materialului marunt (papuci, vopsea, etichete).",
        "mapare_vizuala": "Nivel 1 = Echipamente Mari | Nivel 2 = Material Marunt/BOS."
    }

    db.collection("axon_protocols").document("Project_Manager").set(pm_dna)
    
    print(f"✅ [SUCCESS]: Managerul General a fost sincronizat cu {total_items} repere.")
    print(f"📊 Statistici injectate: {stats_str}")

if __name__ == "__main__":
    flash_sync()
