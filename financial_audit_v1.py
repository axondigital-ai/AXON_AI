import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def run_value_audit():
    print("💰 AXON FINANCE: Pornire Audit de Valoare (Cap. 2 - Echipamente)...")
    print("-" * 80)
    
    # Prețuri Unitare estimate conform Deviz (EUR)
    prices = {
        "LR7-72HGD-685M": 82.50,    # Panouri (aprox. 0.12 EUR/Wp)
        "SUN2000-330KTL-H1": 14200.0, # Invertor
        "STS-7000K-H1": 285000.0,   # Post Transformare
        "SmartLogger3000B": 1250.0,
        "IDM-LTEC-1P-75": 450.0,    # Tracker unit
        "IDM-DRV-LTEC-C": 180.0,    # Drive system
        "IDM-PILE-C120": 42.0,      # Pilon
        "IDM-MC-35-EPDM": 0.85,     # Clemă
        "IDM-TT-OCT-80": 12.40,     # Torque Tube
        "AL-NA2XY-4X185": 18.50,    # Cablu AC
        "GT-404-GALV-FT": 1.15,     # Platbandă
        "ER-1500-BP": 9.00,         # Electrod
        "DC-SOL-6-RED": 0.55,       # Cablu Solar
        "DC-SOL-6-BK": 0.55,
        "MC4-EVO2-1500V": 2.40      # Conectori
    }

    inv_ref = db.collection("axon_inventory")
    docs = inv_ref.stream()
    
    total_general = 0
    
    print(f"{'MATERIAL':<25} | {'CANT':<8} | {'P. UNIT':<10} | {'TOTAL EUR'}")
    print("-" * 80)

    for doc in docs:
        data = doc.to_dict()
        mat = data.get("Material", "N/A")
        cant = data.get("Cantitate_Planificata", 0)
        
        # Luăm prețul din dicționar sau punem 1.0 implicit pentru restul (consumabile)
        p_unit = prices.get(mat, 1.0)
        v_total = cant * p_unit
        
        # Actualizăm documentul cu valorile financiare
        doc.reference.update({
            "Pret_Unitar_EUR": p_unit,
            "Valoare_Totala_EUR": v_total
        })
        
        total_general += v_total
        print(f"{mat[:25]:<25} | {cant:<8} | {p_unit:<10} | {v_total:,.2f}")

    print("-" * 80)
    print(f"VALOARE TOTALĂ CALCULATĂ (CAP. 2): {total_general:,.2f} EUR")
    print(f"VALOARE TARGET (DEVIZ):            1,643,757.00 EUR")
    
    dif = total_general - 1643757
    print(f"DIFERENȚĂ DE CALIBRARE:             {dif:,.2f} EUR")

if __name__ == "__main__":
    run_value_audit()
