import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def handover():
    print("🚚 AXON LOGISTICS: Predare 300 piloni către ALMA Construct...")
    
    # Creăm lotul de custodie pentru ALMA
    alma_lot = {
        "Material": "IDM-PILE-C120 (Lot ALMA)",
        "Categorie": "Mechanical",
        "Cantitate_Planificata": 0,
        "Cantitate_Receptionata": 0,
        "Cantitate_Custodie": 300,
        "Cantitate_Instalata": 0,
        "Contractor_Custodie": "ALMA_CONSTRUCT",
        "Status": "IN_CUSTODIE_MONTAJ"
    }
    db.collection("axon_inventory").document("LOT_PILE_ALMA_01").set(alma_lot)
    print("✅ Succes: ALMA Construct a primit 300 piloni în custodie.")

if __name__ == "__main__":
    handover()
