import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def calibrate_prices():
    print("🎯 AXON FINANCE: Calibrare Prețuri conform Formular F3...")
    
    # Prețuri Unitare REALE extrase din Devizul tău (EUR)
    official_prices = {
        "LR7-72HGD-685M": 60.28,    # Panouri PV
        "SUN2000-330KTL-H1": 7500.0, # Inversoare
        "STS-7000K-H1": 395000.0,   # Stație Transformare
        "SmartLogger3000B": 0.0,     # Inclus în STS
        "IDM-LTEC-1P-75": 1000.0,    # Tracker Unit
        "IDM-DRV-LTEC-C": 500.0,     # Drive System
        "IDM-PILE-C120": 30.0,       # Piloni
        "IDM-MC-35-EPDM": 0.50,      # Cleme
        "IDM-TT-OCT-80": 3.97,       # Tub torsiune
        "AL-NA2XY-4X185": 4.50,      # Cablu AC
        "AL-CU-M12-185": 4.00,       # Papuci
        "EMSKV-63-IP68": 8.50,       # Glande
        "GRM-55-400-G": 2.50,        # Pat cablu
        "AC-SW-80OV-630": 9.95,      # Circuit Breaker
        "DC-SOL-6-RED": 0.45,        # Cablu solar
        "DC-SOL-6-BK": 0.45,         # Cablu solar
        "MC4-EVO2-1500V": 1.80,      # Conectori
        "IDM-JB-800-MC4": 2.00,      # Jumper
        "MC4-Y-ADAPTER": 2.88,       # Y-Branch
        "GT-404-GALV-FT": 1.15,      # Platbandă
        "ER-1500-BP": 9.00,          # Electrod
        "SS-TIE-360-UV": 0.05,       # Coliere
        "PVC-CONDUIT-32": 0.25,      # Tub protecție
        "UV-STR-LAB-SEQ": 0.35,      # Etichete
        "TP-8012-YEL": 2.96          # Marker
    }

    inv_ref = db.collection("axon_inventory")
    docs = inv_ref.stream()
    
    total_modul = 0
    for doc in docs:
        data = doc.to_dict()
        mat = data.get("Material", "")
        cant = data.get("Cantitate_Planificata", 0)
        
        # Aplicăm prețul oficial
        p_unit = official_prices.get(mat, 0.0)
        v_total = cant * p_unit
        
        doc.reference.update({
            "Pret_Unitar_EUR": p_unit,
            "Valoare_Totala_EUR": v_total
        })
        total_modul += v_total
        if p_unit > 0:
            print(f"✅ Calibrat: {mat[:20]}... -> {p_unit} EUR/UM")

    print("-" * 50)
    print(f"💰 VALOARE TOTALĂ ECHIPAMENTE: {total_modul:,.2f} EUR")
    print(f"🎯 TARGET DEVIZ CAP. 2:       1,643,757.00 EUR")
    print(f"⚖️ DIFERENȚĂ FINALĂ:          {total_modul - 1643757:,.2f} EUR")

if __name__ == "__main__":
    calibrate_prices()
