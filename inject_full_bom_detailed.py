import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def inject_full_bom():
    # Datele EXACTE calculate (Per Modul x 44) din documentele tale
    full_bom = [
        # --- 1. MAJOR ASSETS ---
        {"cod": "LR7-72HGD-685M", "n": "Hi-MO 7 Bifacial (685W)", "cat": "Major Assets", "qty": 511500, "um": "buc"},
        {"cod": "SUN2000-330KTL-H1", "n": "Huawei Smart Inverter 330kW", "cat": "Major Assets", "qty": 924, "um": "buc"},
        {"cod": "STS-7000K-H1", "n": "Smart Transformer Station 7MW", "cat": "Major Assets", "qty": 44, "um": "unit"},
        {"cod": "SmartLogger3000B", "n": "Huawei SmartLogger Unit", "cat": "Major Assets", "qty": 44, "um": "buc"},

        # --- 2. MECHANICAL INFRASTRUCTURE ---
        {"cod": "IDM-H1P-TRACK", "n": "Ideamatec Horizon 1P Trackers", "cat": "Mechanical", "qty": 6820, "um": "buc"},
        {"cod": "IDM-PILE-GALV", "n": "Piloni Oțel Galvanizat (Pile)", "cat": "Mechanical", "qty": 47740, "um": "buc"},
        {"cod": "IDM-CLAMP-FIX", "n": "Cleme fixare panouri (Mid/End)", "cat": "Mechanical", "qty": 2046000, "um": "buc"},

        # --- 3. DC ELECTRICAL BOS ---
        {"cod": "CAB-SOLAR-6-TOT", "n": "Cablu Solar 6mm2 (Rosu/Negru)", "cat": "DC Electrical", "qty": 910800, "um": "ml"},
        {"cod": "MC4-EVO2-SET", "n": "Set Conectori MC4-Evo2", "cat": "DC Electrical", "qty": 40920, "um": "set"},
        {"cod": "IDM-JB-800", "n": "Jumper Bypass 800mm MC4", "cat": "DC Electrical", "qty": 6820, "um": "buc"},

        # --- 4. AC & EARTHING ---
        {"cod": "AL-NA2XY-4X185", "n": "Cablu AC Al 4x185mm2", "cat": "AC Electrical", "qty": 122848, "um": "ml"},
        {"cod": "GT-404-GALV-FT", "n": "Platbandă Oțel 40x4mm Galv", "cat": "Earthing", "qty": 136840, "um": "ml"},
        {"cod": "ER-1500-BP", "n": "Electrod Împământare 1.5m", "cat": "Earthing", "qty": 6820, "um": "buc"},
        {"cod": "ACC-LUG-BI", "n": "Papuci Bimetalici Conexiune", "cat": "AC Electrical", "qty": 11088, "um": "buc"},

        # --- 5. CONSUMABLES & MARKING ---
        {"cod": "SS-TIE-360-UV", "n": "Coliere Inox UV Coated", "cat": "Consumables", "qty": 770000, "um": "buc"},
        {"cod": "PVC-CONDUIT-32", "n": "Tub Protecție 32mm UV", "cat": "Consumables", "qty": 29920, "um": "ml"},
        {"cod": "UV-STR-LAB-SEQ", "n": "Etichete Stringuri UV", "cat": "Consumables", "qty": 20460, "um": "buc"},
        {"cod": "TP-8012-YEL", "n": "Marker Torque Vopsea Galben", "cat": "Consumables", "qty": 308, "um": "buc"}
    ]

    print("\n🧬 AXON AI: Sincronizare GESTIUNE TOTALĂ (Full Detail)...")
    for m in full_bom:
        # Respectam Planul de Siguranta: merge=True si mapare Cantitate
        db.collection("axon_inventory").document(m["cod"]).set({
            "Cod_Material": m["cod"],
            "Material": m["n"],
            "Categorie": m["cat"],
            "Cantitate": m["qty"], # Vizibil in v10.8
            "Cantitate_Planificata": m["qty"],
            "Cantitate_Receptionata": 0,
            "Cantitate_Instalata": 0,
            "UM": m["um"],
            "Sursa": "Deviz Detaliat 44 Module"
        }, merge=True)
    print("✅ [FINALIZAT]: Toate materialele (inclusiv cele mărunte) sunt în bază.")

if __name__ == "__main__":
    inject_full_bom()
