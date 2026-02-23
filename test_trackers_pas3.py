import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def validare_trackere():
    print("📋 AXON PM: Validare PV - 5 trackere montate de ALMA...")
    lot_ref = db.collection("axon_inventory").document("LOT_TRK_ALMA")
    doc = lot_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        # Aplicăm Regula Generală de scădere din custodie
        lot_ref.update({
            "Cantitate_Custodie": data.get("Cantitate_Custodie", 0) - 5,
            "Cantitate_Validata": data.get("Cantitate_Validata", 0) + 5,
            "Status": "PROGRES_VALIDAT"
        })
        print("✅ REGULĂ APLICATĂ: 5 trackere s-au transformat din 'Custodie' în 'Realizat'.")

validare_trackere()
