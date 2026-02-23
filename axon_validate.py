import google.cloud.firestore as firestore
db = firestore.Client()

def validate(material_lot_id, cantitate_ok):
    lot_ref = db.collection("axon_inventory").document(material_lot_id)
    # Regula generală: Mutăm din Custodie în Validat
    lot_ref.update({
        "Cantitate_Custodie": firestore.Increment(-cantitate_ok),
        "Cantitate_Validata": firestore.Increment(cantitate_ok),
        "Cantitate_Instalata": firestore.Increment(-cantitate_ok) # Curățăm raportarea
    })
    print(f"✅ Validat {cantitate_ok} unități. Stocul în custodie a scăzut corespunzător.")

if __name__ == "__main__":
    # Exemplu: Validăm 100 piloni la RETA
    validate("LOT_IDM-PILE-C120_RETA", 100)
