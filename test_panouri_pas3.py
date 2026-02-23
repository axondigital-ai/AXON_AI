import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def validare_panouri():
    print("📋 AXON PM: Validare PV - 800 panouri montate de ELMA...")
    lot_ref = db.collection("axon_inventory").document("LOT_PANOURI_ELMA")
    doc = lot_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        cust_actuala = data.get("Cantitate_Custodie", 0)
        valid_anterior = data.get("Cantitate_Validata", 0)
        
        # Aplicăm Regula de Aur
        lot_ref.update({
            "Cantitate_Custodie": cust_actuala - 800,
            "Cantitate_Validata": valid_anterior + 800,
            "Status": "PROGRES_DC_VALIDAT"
        })
        print("✅ REGULĂ APLICATĂ: 800 panouri mutate din 'Custodie' în 'Realizat'.")

validare_panouri()
