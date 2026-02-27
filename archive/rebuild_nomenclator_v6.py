import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def rebuild():
    print("🧹 Resetare Nomenclator...")
    docs = db.collection("axon_nomenclator").stream()
    for doc in docs:
        doc.reference.delete()
    
    print("📚 Construire Nomenclator v6 (Fuzzy Matching enabled)...")
    nom_ref = db.collection("axon_nomenclator")
    
    # Folosim termeni simpli, fara underscores, pentru o cautare mai buna
    rules = [
        ("PILONI", "Foundation", "Mechanical"),
        ("PILE", "Foundation", "Mechanical"),
        ("CLEME", "Module Clamp", "Mechanical"),
        ("MID/END", "Module Clamp", "Mechanical"),
        ("HI-MO", "PV Module", "Major Assets"),
        ("685W", "PV Module", "Major Assets"),
        ("INVERTER", "Inverter", "Major Assets"),
        ("HUAWEI", "Inverter/Logger", "Major Assets"),
        ("TRACKER", "Tracker Unit", "Mechanical"),
        ("IDEAMATEC", "Tracker Unit", "Mechanical"),
        ("CABLU SOLAR", "Solar Cable", "DC Electrical"),
        ("6MM2", "Solar Cable", "DC Electrical"),
        ("CABLU AC", "AC Power Cable", "AC Electrical"),
        ("185MM2", "AC Power Cable", "AC Electrical"),
        ("STS", "Transformer Station", "Major Assets"),
        ("7MW", "Transformer Station", "Major Assets"),
        ("TRANSFORMER", "Transformer Station", "Major Assets"),
        ("PAPUCI", "Electrical Lugs", "DC Electrical"),
        ("IMPAMANTARE", "Earthing System", "Earthing"),
        ("PLATBANDA", "Earthing System", "Earthing"),
        ("ELECTROD", "Earthing System", "Earthing"),
        ("MC4", "Connectors", "DC Electrical"),
        ("TUB", "Protection Tube", "Consumables"),
        ("COLIERE", "Fastening UV", "Consumables"),
        ("MARKER", "Marking Tool", "Consumables"),
        ("ETICHETE", "Identification", "Consumables")
    ]
    
    for termen, pv, cat in rules:
        safe_id = termen.replace("/", "_").replace(" ", "_")
        nom_ref.document(safe_id).set({
            "termen": termen,
            "pvcase": pv,
            "cat": cat
        })
    print("✅ Nomenclator v6 configurat.")

if __name__ == "__main__":
    rebuild()
