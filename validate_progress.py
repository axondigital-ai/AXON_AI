import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def validate():
    print("📋 AXON PM: Se efectuează recepția calitativă pentru piloni...")
    
    # Căutăm lotul raportat de RETA
    docs = db.collection("axon_inventory").where("Material", "==", "IDM-PILE-C120").stream()
    
    for doc in docs:
        d = doc.to_dict()
        if "Lot" not in d.get("Material", ""): # Mergem pe master record în simularea asta
            raportat = d.get("Cantitate_Instalata", 0)
            if raportat > 0:
                # Validăm 180 din cei 200
                doc.reference.update({
                    "Cantitate_Validata": 180,
                    "Status": "VALIDAT_PARTIAL"
                })
                print(f"✅ Recepție finalizată: 180 piloni validați și trecuți în raportul EPC.")

if __name__ == "__main__":
    validate()
