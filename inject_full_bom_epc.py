import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def inject_detailed_inventory():
    # Definim nomenclatorul complet (100% conform PDF-urilor tale)
    full_inventory = [
        # --- MAJOR ASSETS ---
        {"cod": "LR7-72HGD-685M", "nume": "PV Modules Longi 685W", "cat": "Major Assets", "qty": 511500, "um": "buc"},
        {"cod": "SUN2000-330KTL-H1", "nume": "Huawei Inverters 330kW", "cat": "Major Assets", "qty": 924, "um": "buc"},
        {"cod": "STS-7000K-H1", "nume": "Smart Transformer Stations", "cat": "Major Assets", "qty": 44, "um": "unit"},
        
        # --- MECHANICAL BOS ---
        {"cod": "IDM-H1P-TRACK", "nume": "Ideamatec Horizon 1P Trackers", "cat": "Mechanical BOS", "qty": 6820, "um": "buc"},
        {"cod": "IDM-PILE-GALV", "nume": "Piloni Structura (Galvanizati)", "cat": "Mechanical BOS", "qty": 47740, "um": "buc"},
        {"cod": "IDM-CLAMP-FIX", "nume": "Cleme fixare panouri (Mid/End)", "cat": "Mechanical BOS", "qty": 2046000, "um": "buc"},
        
        # --- DC ELECTRICAL BOS ---
        {"cod": "CAB-SOLAR-6-TOT", "nume": "Cablu Solar 6mm2 (Rosu/Negru)", "cat": "DC Electrical BOS", "qty": 910800, "um": "ml"},
        {"cod": "MC4-EVO2-SET", "nume": "Set Conectori MC4-EVO2", "cat": "DC Electrical BOS", "qty": 40920, "um": "set"},
        {"cod": "IDM-JB-800", "nume": "Jumper Bypass 800mm MC4", "cat": "DC Electrical BOS", "qty": 6820, "um": "buc"},
        
        # --- AC & EARTHING BOS ---
        {"cod": "AL-NA2XY-4X185", "nume": "Cablu AC Al 4x185mm2", "cat": "AC Electrical BOS", "qty": 122848, "um": "ml"},
        {"cod": "GT-404-GALV", "nume": "Platbanda Otel 40x4mm Galv", "cat": "Earthing", "qty": 136840, "um": "ml"},
        {"cod": "ER-1500-BP", "nume": "Electrod Impamantare 1.5m", "cat": "Earthing", "qty": 6820, "um": "buc"},
        {"cod": "SS-TIE-360-UV", "nume": "Coliere Inox UV Coated", "cat": "Consumables", "qty": 770000, "um": "buc"}
    ]

    print("\n🧬 AXON AI: Sincronizare GESTIUNE DE DETALIU (Full EPC Scale)...")
    for m in full_inventory:
        db.collection("axon_inventory").document(m["cod"]).set({
            "Data_Initializare": "2026-02-22",
            "Cod_Material": m["cod"],
            "Material": m["nume"],
            "Categorie": m["cat"],
            "Cantitate_Planificata": m["qty"],
            "Cantitate_Receptionata": 0,
            "Cantitate_Instalata": 0,
            "UM": m["um"],
            "Status": "Planned"
        }, merge=True)
        print(f"   📦 Adaugat: {m['nume']} ({m['qty']} {m['um']})")

    print("\n✅ [FINALIZAT]: Gestiunea de detaliu este activa in v10.8.")

if __name__ == "__main__":
    inject_detailed_inventory()
