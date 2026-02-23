import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def fix():
    # Fix Master Record
    piloni = db.collection("axon_inventory").where("Material", "==", "IDM-PILE-C120").stream()
    for doc in piloni:
        if "Lot" not in doc.to_dict().get("Material", ""):
            doc.reference.update({"Cantitate_Validata": 145, "Cantitate_Instalata": 0})
    
    # Fix Lot RETA
    lot_reta = db.collection("axon_inventory").document("LOT_PILE_RETA_START")
    if lot_reta.get().exists:
        lot_reta.update({"Cantitate_Validata": 145, "Cantitate_Instalata": 150})
        print("✅ Date sincronizate: Validat=145, Raportat=150")

fix()
