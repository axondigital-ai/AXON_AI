import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def receptie_trackere():
    print("🚛 AXON: Recepție 44 Trackere (Major Assets)...")
    # Căutăm codul de tracker în inventar
    docs = db.collection("axon_inventory").where("Material", "==", "IDM-TRK-S1").stream()
    for doc in docs:
        doc.reference.update({
            "Cantitate_Receptionata": 44,
            "Status": "STOC_CENTRAL_ASSETS"
        })
    print("✅ Succes: 44 trackere sunt în Depozit.")

receptie_trackere()
