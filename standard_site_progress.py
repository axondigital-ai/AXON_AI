import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def update_progress():
    print("🏗️ AXON: Se procesează încă 50 de piloni pentru RETA...")
    doc_ref = db.collection("axon_inventory").document("LOT_PILE_RETA_START")
    doc = doc_ref.get()
    
    if doc.exists:
        data = doc.to_dict()
        # Luăm valorile actuale
        raportat_vechi = data.get("Cantitate_Instalata", 0)
        validat_vechi = data.get("Cantitate_Validata", 0)
        custodie_veche = data.get("Cantitate_Custodie", 0)
        
        # Actualizăm valorile: adăugăm 50
        doc_ref.update({
            "Cantitate_Instalata": raportat_vechi + 50,
            "Cantitate_Validata": validat_vechi + 50,
            "Cantitate_Custodie": custodie_veche - 50,
            "Status": "MONTAJ_IN_PROGRES"
        })
        print(f"✅ Lot RETA actualizat: {validat_vechi + 50} piloni validați în total.")

if __name__ == "__main__":
    update_progress()
