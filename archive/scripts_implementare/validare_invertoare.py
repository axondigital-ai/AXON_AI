import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def validare():
    print("📋 AXON PM: Validare PV pentru 5 invertoare...")
    lot_ref = db.collection("axon_inventory").document("LOT_INV_ELMA")
    doc = lot_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        cust_actuala = data.get("Cantitate_Custodie", 0)
        
        # REGULA DE AUR: Scădem din Custodie, adunăm la Validat
        lot_ref.update({
            "Cantitate_Custodie": cust_actuala - 5,
            "Cantitate_Validata": firestore.Increment(5),
            "Status": "MONTAJ_CERTIFICAT"
        })
        print("✅ REGULĂ APLICATĂ: 5 invertoare au devenit progres oficial.")

validare()
