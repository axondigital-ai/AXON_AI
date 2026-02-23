import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def setup_nomenclator():
    print("📚 AXON: Actualizare Nomenclator Complet...")
    nom_ref = db.collection("axon_nomenclator")
    
    nomenclator_data = [
        # Structură & Mecanică
        {"termen": "PILONI", "pvcase": "Foundation", "cat": "Mechanical"},
        {"termen": "PILE", "pvcase": "Foundation", "cat": "Mechanical"},
        {"termen": "CLEME", "pvcase": "Module Clamp", "cat": "Mechanical"},
        {"termen": "MID/END", "pvcase": "Module Clamp", "cat": "Mechanical"},
        {"termen": "TRACKERS", "pvcase": "Tracker Unit", "cat": "Mechanical"},
        {"termen": "IDEAMATEC", "pvcase": "Tracker Unit", "cat": "Mechanical"},
        {"termen": "JUMPER", "pvcase": "Jumper Cable", "cat": "Mechanical"},
        
        # Panouri & Inversoare
        {"termen": "HI-MO", "pvcase": "PV Module", "cat": "Major Assets"},
        {"termen": "685W", "pvcase": "PV Module", "cat": "Major Assets"},
        {"termen": "330KW", "pvcase": "Inverter", "cat": "Major Assets"},
        {"termen": "STS-7000", "pvcase": "Transformer Station", "cat": "Major Assets"},
        {"termen": "SMARTLOGGER", "pvcase": "Communication Unit", "cat": "Major Assets"},
        
        # Electrice & Cabluri
        {"termen": "CABLU SOLAR", "pvcase": "Solar Cable", "cat": "DC Electrical"},
        {"termen": "6MM2", "pvcase": "Solar Cable", "cat": "DC Electrical"},
        {"termen": "CABLU AC", "pvcase": "AC Power Cable", "cat": "AC Electrical"},
        {"termen": "185MM2", "pvcase": "AC Power Cable", "cat": "AC Electrical"},
        {"termen": "MC4", "pvcase": "Connectors", "cat": "DC Electrical"},
        {"termen": "PAPUCI", "pvcase": "Electrical Lugs", "cat": "DC Electrical"},
        
        # Împământare & Protecție
        {"termen": "ÎMPĂMÂNTARE", "pvcase": "Earthing System", "cat": "Earthing"},
        {"termen": "PLATBANDA", "pvcase": "Earthing System", "cat": "Earthing"},
        {"termen": "TUB", "pvcase": "Protection Tube", "cat": "Consumables"},
        {"termen": "COLIERE", "pvcase": "Fastening UV", "cat": "Consumables"},
        {"termen": "MARKER", "pvcase": "Marking Tool", "cat": "Consumables"},
        {"termen": "ETICHETE", "pvcase": "Identification", "cat": "Consumables"}
    ]
    
    for item in nomenclator_data:
        safe_id = item["termen"].replace("/", "_")
        nom_ref.document(safe_id).set(item)
        print(f"✔️ Nomenclator: {item['termen']} -> {item['pvcase']}")

if __name__ == "__main__":
    setup_nomenclator()
