import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def handover_trackere():
    print("🤝 AXON: Predare 20 trackere către ALMA...")
    # Creăm lotul de custodie pentru ALMA
    db.collection("axon_inventory").document("LOT_TRK_ALMA").set({
        "Material": "IDM-TRK-S1 (ALMA)",
        "Categorie": "Major Assets",
        "Cantitate_Custodie": 20,
        "Cantitate_Validata": 0,
        "Contractor_Custodie": "ALMA_CONSTRUCT",
        "Status": "MONTAJ_SISTEM"
    })
    print("✅ Succes: 20 trackere predate către ALMA.")

handover_trackere()
