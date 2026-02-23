import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def update_to_epc_standards():
    # 1. Ștergem datele vechi (curățăm "zgomotul")
    docs = db.collection("axon_inventory").stream()
    for doc in docs:
        doc.reference.delete()

    # 2. Injectăm doar Componentele Principale conform standardelor Tier 1 EPC
    epc_main_list = [
        {"cod": "LR7-72HGD-685M", "nume": "PV Modules (Tier 1 Bifacial)", "qty": 511500, "um": "buc"},
        {"cod": "IDM-H1P-TRACK", "nume": "Tracker Systems (Ideamatec Horizon 1P)", "qty": 6820, "um": "buc"},
        {"cod": "SUN2000-330KTL-H1", "nume": "Power Inverters (Huawei 330kW)", "qty": 924, "um": "buc"},
        {"cod": "STS-7000K-H1", "nume": "Power Stations (Huawei STS 7MW)", "qty": 44, "um": "unit"},
        {"cod": "CAB-6-DC-TOTAL", "nume": "DC Cabling (Solar 6mm2 Red/Blk)", "qty": 910800, "um": "ml"},
        {"cod": "AL-NA2XY-4X185", "nume": "AC Power Cables (Medium Voltage Al)", "qty": 122848, "um": "ml"},
        {"cod": "SMART-LOGGER-3000", "nume": "SCADA & Monitoring (SmartLogger)", "qty": 44, "um": "buc"}
    ]

    print("\n🧬 AXON AI: Sincronizare Dashboard EPC (Tier 1 Standards)...")
    for m in epc_main_list:
        db.collection("axon_inventory").document(m["cod"]).set({
            "Data": "2026-02-22",
            "Cod_Material": m["cod"],
            "Material": m["nume"],
            "Cantitate": m["qty"],
            "Tip": "Main Equipment",
            "Sursă": "ROGVAIV EPC Master BOM"
        })
    print("🔥 [FINALIZAT]: Dashboard-ul a fost curățat de consumabile. Avem doar 7 linii strategice.")

if __name__ == "__main__":
    update_to_epc_standards()
