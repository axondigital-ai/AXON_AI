import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def simulate_reception():
    print("🚛 AXON LOGISTICS: Recepție 1.500 panouri PV în depozit...")
    inv_ref = db.collection("axon_inventory")
    
    # Căutăm panourile PV (Master Record)
    docs = inv_ref.where("Material", "==", "LR7-72HGD-685M").stream()
    
    for doc in docs:
        doc.reference.update({
            "Cantitate_Receptionata": 1500,
            "Status": "IN_DEPOZIT_CENTRAL"
        })
        print("✅ Panouri PV: 1.500 bucăți înregistrate în Stoc Central.")

simulate_reception()
