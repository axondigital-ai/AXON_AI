import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def update_to_tier1_standards():
    # 1. Ștergere completă pentru reinițializare curată
    docs = db.collection("axon_inventory").stream()
    for doc in docs:
        doc.reference.delete()

    # 2. Datele Exacte (44 module x valorile din PDF)
    epc_master_list = [
        {"cod": "PV-MOD-LONG-685", "nume": "Major: PV Modules (Longi 685W Bifacial)", "qty": 511500, "um": "buc"},
        {"cod": "TRK-IDM-HORIZON", "nume": "Major: Tracker Systems (Ideamatec 1P)", "qty": 6820, "um": "buc"},
        {"cod": "INV-HUA-330KTL", "nume": "Major: Power Inverters (Huawei 330kW)", "qty": 924, "um": "buc"},
        {"cod": "STS-HUA-7000K", "nume": "Major: Transformer Stations (Huawei 7MW)", "qty": 44, "um": "unit"},
        {"cod": "CAB-DC-SOLAR-6", "nume": "BOS: DC Solar Cabling (Total Red/Blk)", "qty": 910800, "um": "ml"},
        {"cod": "CAB-AC-MV-AL-185", "nume": "BOS: AC MV Power Cables (Al 185mmp)", "qty": 122848, "um": "ml"},
        {"cod": "COMM-SCADA-LOG", "nume": "BOS: SCADA & Communication (SmartLogger)", "qty": 44, "um": "buc"}
    ]

    print("\n🧬 AXON AI: Sincronizare Dashboard Executiv (Tier 1 Standards)...")
    for m in epc_master_list:
        db.collection("axon_inventory").document(m["cod"]).set({
            "Data": "2026-02-22",
            "Cod_Material": m["cod"],
            "Material": m["nume"],
            "Cantitate": m["qty"],
            "Tip": "Strategic Asset",
            "Sursă": "ROGVAIV Master BOM (44 Modules)"
        })
        print(f"   ✅ [STRATEGIC]: {m['nume']} - {m['qty']} {m['um']}")
    
    print("\n🔥 [FINALIZAT]: Interfața v10.8 afișează acum doar Componentele Principale.")

if __name__ == "__main__":
    update_to_tier1_standards()
