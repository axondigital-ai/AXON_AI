import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def setup_nomenclator():
    print("📚 AXON: Actualizare Nomenclator la versiunea v4 (Full Coverage)...")
    nom_ref = db.collection("axon_nomenclator")
    
    nomenclator_data = [
        # Mecanică & Structură
        {"termen": "PILONI", "pvcase": "Foundation", "cat": "Mechanical"},
        {"termen": "PILE", "pvcase": "Foundation", "cat": "Mechanical"},
        {"termen": "CLEME", "pvcase": "Module Clamp", "cat": "Mechanical"},
        {"termen": "MID/END", "pvcase": "Module Clamp", "cat": "Mechanical"},
        {"termen": "TRACKERS", "pvcase": "Tracker Unit", "cat": "Mechanical"},
        {"termen": "IDEAMATEC", "pvcase": "Tracker Unit", "cat": "Mechanical"},
        {"termen": "JUMPER", "pvcase": "Jumper Cable", "cat": "Mechanical"},
        
        # Echipamente Principale
        {"termen": "HI-MO", "pvcase": "PV Module", "cat": "Major Assets"},
        {"termen": "685W", "pvcase": "PV Module", "cat": "Major Assets"},
        {"termen": "330KW", "pvcase": "Inverter", "cat": "Major Assets"},
        {"termen": "HUAWEI", "pvcase": "Inverter/Logger", "cat": "Major Assets"},
        {"termen": "TRANSFORMER", "pvcase": "Transformer Station", "cat": "Major Assets"},
        {"termen": "7MW", "pvcase": "Transformer Station", "cat": "Major Assets"},
        {"termen": "STATION", "pvcase": "Transformer Station", "cat": "Major Assets"},
        
        # Electrice & DC/AC
        {"termen": "CABLU SOLAR", "pvcase": "Solar Cable", "cat": "DC Electrical"},
        {"termen": "6MM2", "pvcase": "Solar Cable", "cat": "DC Electrical"},
        {"termen": "CABLU AC", "pvcase": "AC Power Cable", "cat": "AC Electrical"},
        {"termen": "185MM2", "pvcase": "AC Power Cable", "cat": "AC Electrical"},
        {"termen": "MC4", "pvcase": "Connectors", "cat": "DC Electrical"},
        {"termen": "PAPUCI", "pvcase": "Electrical Lugs", "cat": "DC Electrical"},
        
        # Împământare (Inclusiv Diacritice)
        {"termen": "ÎMPĂMÂNTARE", "pvcase": "Earthing System", "cat": "Earthing"},
        {"termen": "PLATBANDA", "pvcase": "Earthing System", "cat": "Earthing"},
        {"termen": "PLATBANDĂ", "pvcase": "Earthing System", "cat": "Earthing"},
        {"termen": "ELECTROD", "pvcase": "Earthing System", "cat": "Earthing"},
        
        # Consumabile
        {"termen": "TUB", "pvcase": "Protection Tube", "cat": "Consumables"},
        {"termen": "COLIERE", "pvcase": "Fastening UV", "cat": "Consumables"},
        {"termen": "MARKER", "pvcase": "Marking Tool", "cat": "Consumables"},
        {"termen": "ETICHETE", "pvcase": "Identification", "cat": "Consumables"}
    ]
    
    for item in nomenclator_data:
        safe_id = item["termen"].replace("/", "_").replace(" ", "_")
        nom_ref.document(safe_id).set(item)
        print(f"✔️ Nomenclator: {item['termen']} -> {item['pvcase']}")

if __name__ == "__main__":
    setup_nomenclator()
