import google.cloud.firestore as firestore
import os

# Configurare Proiect
PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def populate_axon_data():
    # 1. Nomenclator Materiale (Master BOM 44 Module)
    materials = [
        {"cod": "LR7-72HGD-685M", "nume": "Panou Longi Hi-MO 7 (685W)", "qty": 511500, "um": "buc"},
        {"cod": "IDM-H1P-TRACK", "nume": "Tracker Ideamatec Horizon 1P", "qty": 6820, "um": "buc"},
        {"cod": "SUN2000-330KTL-H1", "nume": "Invertor Huawei 330kW", "qty": 924, "um": "buc"},
        {"cod": "STS-7000K-H1", "nume": "Statie Huawei STS 7MW", "qty": 44, "um": "unit"},
        {"cod": "SS-TIE-360-UV", "nume": "Coliere Inox UV Coated", "qty": 770000, "um": "buc"},
        {"cod": "GT-404-GALV-FT", "nume": "Platbanda Otel Zincat 40x4", "qty": 136840, "um": "ml"}
    ]

    print("\n🧬 AXON AI: Se injectează Nomenclatorul de Materiale...")
    for m in materials:
        db.collection("axon_inventory").document(m["cod"]).set({
            "Data": "2026-02-22",
            "Cod_Material": m["cod"],
            "Material": m["nume"],
            "Cantitate": m["qty"],
            "Tip": "Planificat",
            "Sursă": "Master BOM ROGVAIV (BNEF 2026)"
        })
        print(f"   ✅ Adăugat: {m['nume']}")

    # 2. Norme de Constructie
    norms = [
        {"id": "STR-01", "lucrare": "Montaj Tracker (Mecanic)", "norma": 32.0, "um": "buc"},
        {"id": "PV-01", "lucrare": "Montaj Panou Fotovoltaic", "norma": 0.25, "um": "buc"},
        {"id": "EL-01", "lucrare": "Conexiune Invertor AC/DC", "norma": 12.0, "um": "buc"}
    ]

    print("\n🏗️ AXON AI: Se injectează Normele de Lucru EPC...")
    for n in norms:
        db.collection("axon_norms").document(n["id"]).set(n)
        print(f"   ✅ Normă setată: {n['lucrare']}")

    print("\n🔥 [MISIUNE ÎNDEPLINITĂ]: Baza de date AXON AI a fost populată.")

if __name__ == "__main__":
    populate_axon_data()
