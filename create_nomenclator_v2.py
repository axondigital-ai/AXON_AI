import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def setup_nomenclator():
    print("📚 AXON: Construire Tabel Nomenclator (Versiunea Securizată)...")
    nom_ref = db.collection("axon_nomenclator")
    
    nomenclator_data = [
        {"termen": "PILONI", "pvcase": "Foundation", "cat": "Mechanical"},
        {"termen": "PILE", "pvcase": "Foundation", "cat": "Mechanical"},
        {"termen": "CLEME", "pvcase": "Module Clamp", "cat": "Mechanical"},
        {"termen": "MID/END", "pvcase": "Module Clamp", "cat": "Mechanical"},
        {"termen": "HI-MO", "pvcase": "PV Module", "cat": "Major Assets"},
        {"termen": "685W", "pvcase": "PV Module", "cat": "Major Assets"},
        {"termen": "330KW", "pvcase": "Inverter", "cat": "Major Assets"},
        {"termen": "TRACKERS", "pvcase": "Tracker Unit", "cat": "Mechanical"},
        {"termen": "IDEAMATEC", "pvcase": "Tracker Unit", "cat": "Mechanical"},
        {"termen": "STS-7000", "pvcase": "Transformer Station", "cat": "Major Assets"},
        {"termen": "CABLU SOLAR", "pvcase": "Solar Cable", "cat": "DC Electrical"},
        {"termen": "CABLU AC", "pvcase": "AC Power Cable", "cat": "AC Electrical"},
        {"termen": "ÎMPĂMÂNTARE", "pvcase": "Earthing System", "cat": "Earthing"},
        {"termen": "PLATBANDA", "pvcase": "Earthing System", "cat": "Earthing"}
    ]
    
    for item in nomenclator_data:
        # Înlocuim "/" cu "_" pentru a nu induce Firestore în eroare
        safe_id = item["termen"].replace("/", "_")
        nom_ref.document(safe_id).set(item)
        print(f"✔️ Adăugat în nomenclator: {item['termen']} -> {item['pvcase']}")

if __name__ == "__main__":
    setup_nomenclator()
