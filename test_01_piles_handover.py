import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def phase_1():
    print("📦 AXON LOGISTICS: Faza 1 - Recepție și Handover Piloni...")
    inv_ref = db.collection("axon_inventory")
    
    # 1. Recepția Master (Intră în șantier)
    master_query = inv_ref.where("Material", "==", "IDM-PILE-C120").stream()
    for doc in master_query:
        doc.reference.update({
            "Cantitate_Receptionata": 1085,
            "Status": "RECEPȚIONAT_TOTAL"
        })
        print("✅ Piloni Recepționați: 1.085 buc (Stoc Proiect)")

    # 2. Creare Lot Custodie RETA (Predare 600 buc)
    lot_id = "LOT_PILE_RETA_START"
    lot_data = {
        "Material": "IDM-PILE-C120 (Lot RETA)",
        "Categorie": "Mechanical",
        "Cantitate_Planificata": 0,
        "Cantitate_Receptionata": 0,
        "Cantitate_Custodie": 600,
        "Cantitate_Instalata": 0,  # Raportat
        "Cantitate_Validata": 0,   # Validat
        "Contractor_Custodie": "RETA_CONSTRUCT",
        "Status": "ÎN_CUSTODIE_MONTAJ"
    }
    db.collection("axon_inventory").document(lot_id).set(lot_data)
    print("🤝 Custodie: 600 piloni predați către RETA_CONSTRUCT.")

if __name__ == "__main__":
    phase_1()
