import sys
import google.cloud.firestore as firestore
db = firestore.Client()

def handover(material_baza, cantitate, contractor):
    # 1. Scădem din Master (Recepția rămâne, dar marcăm că a plecat în custodie)
    master_ref = db.collection("axon_inventory").where("Material", "==", material_baza).get()[0].reference
    master_ref.update({"Cantitate_Custodie": firestore.Increment(cantitate)})
    
    # 2. Creăm/Actualizăm Lotul Contractorului
    lot_id = f"LOT_{material_baza}_{contractor}".replace(" ", "_")
    db.collection("axon_inventory").document(lot_id).set({
        "Material": f"{material_baza} ({contractor})",
        "Categorie": master_ref.get().to_dict()['Categorie'],
        "Cantitate_Custodie": firestore.Increment(cantitate),
        "Contractor_Custodie": contractor,
        "Status": "IN_LUCRU"
    }, merge=True)
    print(f"✅ Transmis {cantitate} unități de {material_baza} către {contractor}")

if __name__ == "__main__":
    # Exemplu: Predăm 500 piloni la RETA
    handover("IDM-PILE-C120", 500, "RETA")
