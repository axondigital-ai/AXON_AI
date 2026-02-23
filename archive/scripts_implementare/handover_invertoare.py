import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def handover():
    print("🤝 AXON: Predare 10 invertoare către ELMA...")
    # Creăm lotul de custodie
    db.collection("axon_inventory").document("LOT_INV_ELMA").set({
        "Material": "SUN2000-330KTL-H1 (ELMA)",
        "Categorie": "Major Assets",
        "Cantitate_Custodie": 10,
        "Cantitate_Validata": 0,
        "Cantitate_Planificata": 0, # Planificarea rămâne în Master
        "Contractor_Custodie": "ELMA_CONSTRUCT",
        "Status": "PREGĂTIRE_MONTAJ"
    })
    print("✅ Handover finalizat. 10 invertoare sunt acum în teren.")

handover()
