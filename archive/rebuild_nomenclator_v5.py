import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def rebuild():
    print("🧹 Curățare Nomenclator vechi...")
    docs = db.collection("axon_nomenclator").stream()
    for doc in docs:
        doc.reference.delete()
    
    print("📚 Construire Nomenclator v5 (Fără erori)...")
    nom_ref = db.collection("axon_nomenclator")
    
    rules = [
        ("PILONI", "Foundation", "Mechanical"),
        ("CLEME", "Module Clamp", "Mechanical"),
        ("PANOURI", "PV Module", "Major Assets"),
        ("HI-MO", "PV Module", "Major Assets"),
        ("685W", "PV Module", "Major Assets"),
        ("INVERTER", "Inverter", "Major Assets"),
        ("HUAWEI", "Inverter/Logger", "Major Assets"),
        ("TRACKER", "Tracker Unit", "Mechanical"),
        ("IDEAMATEC", "Tracker Unit", "Mechanical"),
        ("CABLU_SOLAR", "Solar Cable", "DC Electrical"),
        ("6MM2", "Solar Cable", "DC Electrical"),
        ("CABLU_AC", "AC Power Cable", "AC Electrical"),
        ("STS", "Transformer Station", "Major Assets"),
        ("7MW", "Transformer Station", "Major Assets"),
        ("PAPUCI", "Electrical Lugs", "DC Electrical"),
        ("IMPAMANTARE", "Earthing System", "Earthing"),
        ("PLATBANDA", "Earthing System", "Earthing"),
        ("ELECTROD", "Earthing System", "Earthing"),
        ("MC4", "Connectors", "DC Electrical")
    ]
    
    for termen, pv, cat in rules:
        nom_ref.document(termen).set({
            "termen": termen,
            "pvcase": pv,
            "cat": cat
        })
    print("✅ Nomenclator v5 gata.")

if __name__ == "__main__":
    rebuild()
