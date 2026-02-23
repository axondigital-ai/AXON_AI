import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def set_dynamic_logic():
    print("⚙️ AXON: Activare calcul dinamic (eliminare hardcoding)...")
    inv_ref = db.collection("axon_inventory")
    
    # 1. Curățăm Master Record-ul (să nu mai aibă cifre de progres)
    master_docs = inv_ref.where("Material", "==", "IDM-PILE-C120").stream()
    for doc in master_docs:
        # Verificăm să fie cel fără paranteze
        if "(" not in doc.to_dict().get("Material", ""):
            doc.reference.update({
                "Cantitate_Receptionata": 1085,
                "Cantitate_Validata": 0,  # Master-ul nu "produce", el doar "conține"
                "Cantitate_Instalata": 0
            })
            print("✅ Master Record curățat. (Validat setat pe 0)")

    # 2. Ne asigurăm că Lotul RETA este singura sursă de adevăr pentru progres
    lot_ref = db.collection("axon_inventory").document("LOT_PILE_RETA_START")
    if lot_ref.get().exists:
        lot_ref.update({
            "Cantitate_Validata": 145,
            "Cantitate_Instalata": 150,
            "Cantitate_Receptionata": 0 # Lotul nu dublează recepția
        })
        print("✅ Lot RETA setat ca sursă de calcul (145 Validați).")

if __name__ == "__main__":
    set_dynamic_logic()
