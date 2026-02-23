import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def receptie_panouri():
    print("🚛 AXON: Recepție 11.625 Panouri (LR7-72HGD-685M)...")
    docs = db.collection("axon_inventory").where("Material", "==", "LR7-72HGD-685M").stream()
    for doc in docs:
        doc.reference.update({
            "Cantitate_Receptionata": 11625,
            "Status": "STOC_CENTRAL_PANOURI"
        })
    print("✅ Succes: Toate panourile sunt acum în Depozitul Central.")

receptie_panouri()
