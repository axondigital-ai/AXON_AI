import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def receptie():
    print("🚛 AXON: Recepție 1.085 piloni...")
    # Căutăm Master Record-ul (cel fără paranteze în nume)
    docs = db.collection("axon_inventory").where("Material", "==", "IDM-PILE-C120").stream()
    for doc in docs:
        doc.reference.update({
            "Cantitate_Receptionata": 1085,
            "Status": "STOC_CENTRAL"
        })
    print("✅ Succes: 1.085 piloni sunt acum 'În Depozit'.")

receptie()
