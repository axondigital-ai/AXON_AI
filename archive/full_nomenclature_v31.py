import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def reset_nom():
    print("🧹 Resetare Nomenclator Master (25/25 articole)...")
    for doc in db.collection("axon_nomenclator").stream():
        doc.reference.delete()
    
    nom_data = [
        # Major Assets
        {"termen": "LR7-72HGD", "pv": "PV Module", "cat": "Major Assets"},
        {"termen": "SUN2000-330KTL", "pv": "Inverter", "cat": "Major Assets"},
        {"termen": "STS-7000K", "pv": "Transformer Station", "cat": "Major Assets"},
        {"termen": "SmartLogger3000B", "pv": "Communication Unit", "cat": "Major Assets"},
        # Mechanical
        {"termen": "IDM-LTEC", "pv": "Tracker Unit", "cat": "Mechanical"},
        {"termen": "IDM-DRV", "pv": "Drive System", "cat": "Mechanical"},
        {"termen": "IDM-PILE", "pv": "Foundation", "cat": "Mechanical"},
        {"termen": "IDM-MC-35", "pv": "Module Clamp", "cat": "Mechanical"},
        {"termen": "IDM-TT-OCT", "pv": "Torque Tube", "cat": "Mechanical"},
        {"termen": "IDM-JB-800", "pv": "Jumper Cable", "cat": "Mechanical"},
        # DC Electrical
        {"termen": "DC-SOL-6", "pv": "Solar Cable", "cat": "DC Electrical"},
        {"termen": "MC4-EVO2", "pv": "Connectors", "cat": "DC Electrical"},
        {"termen": "MC4-Y-ADAPTER", "pv": "Y-Branch", "cat": "DC Electrical"},
        {"termen": "EMSKV-63", "pv": "M63 Gland", "cat": "DC Electrical"},
        {"termen": "AL-CU-M12-185", "pv": "Electrical Lugs", "cat": "DC Electrical"},
        # AC Electrical
        {"termen": "AL-NA2XY", "pv": "AC Power Cable", "cat": "AC Electrical"},
        {"termen": "GRM-55-400", "pv": "Cable Tray", "cat": "AC Electrical"},
        {"termen": "AC-SW-80OV", "pv": "AC Protection", "cat": "AC Electrical"},
        # Earthing
        {"termen": "GT-404-GALV", "pv": "Earthing System", "cat": "Earthing"},
        {"termen": "ER-1500-BP", "pv": "Earth Rod", "cat": "Earthing"},
        # Consumables
        {"termen": "SS-TIE-360", "pv": "Cable Ties", "cat": "Consumables"},
        {"termen": "PVC-CONDUIT", "pv": "Protection Tube", "cat": "Consumables"},
        {"termen": "UV-STR-LAB", "pv": "Identification", "cat": "Consumables"},
        {"termen": "TP-8012-YEL", "pv": "Marking Tool", "cat": "Consumables"}
    ]
    
    for item in nom_data:
        db.collection("axon_nomenclator").document(item["termen"]).set(item)
    print("✅ Nomenclator complet sincronizat.")

if __name__ == "__main__":
    reset_nom()
