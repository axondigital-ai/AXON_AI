import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def handover_panouri():
    print("🤝 AXON: Predare 2.500 panouri către ELMA...")
    # Creăm lotul de custodie pentru ELMA
    db.collection("axon_inventory").document("LOT_PANOURI_ELMA").set({
        "Material": "LR7-72HGD-685M (ELMA)",
        "Categorie": "Major Assets",
        "Cantitate_Custodie": 2500,
        "Cantitate_Validata": 0,
        "Contractor_Custodie": "ELMA_CONSTRUCT",
        "Status": "MONTAJ_DC"
    })
    print("✅ Succes: 2,500 panouri predate către ELMA.")

handover_panouri()
