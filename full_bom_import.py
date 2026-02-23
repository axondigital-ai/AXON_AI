import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def import_missing_items():
    print("🚀 AXON: Incepere Import Master BOM (25 repere)...")
    inv_ref = db.collection("axon_inventory")
    
    # Lista completa din Deviz si BOM
    master_bom = [
        {"Material": "LR7-72HGD-685M", "Cantitate": 11625, "UM": "buc", "Cat": "Major Assets", "PV": "PV Module"},
        {"Material": "SUN2000-330KTL-H1", "Cantitate": 21, "UM": "buc", "Cat": "Major Assets", "PV": "Inverter"},
        {"Material": "STS-7000K-H1", "Cantitate": 1, "UM": "unit", "Cat": "Major Assets", "PV": "Transformer Station"},
        {"Material": "SmartLogger3000B", "Cantitate": 1, "UM": "buc", "Cat": "Major Assets", "PV": "Communication Unit"},
        {"Material": "IDM-LTEC-1P-75", "Cantitate": 155, "UM": "set", "Cat": "Mechanical", "PV": "Tracker Unit"},
        {"Material": "IDM-DRV-LTEC-C", "Cantitate": 155, "UM": "set", "Cat": "Mechanical", "PV": "Drive System"},
        {"Material": "IDM-PILE-C120", "Cantitate": 1085, "UM": "buc", "Cat": "Mechanical", "PV": "Foundation"},
        {"Material": "IDM-MC-35-EPDM", "Cantitate": 46500, "UM": "buc", "Cat": "Mechanical", "PV": "Module Clamp"},
        {"Material": "IDM-TT-OCT-80", "Cantitate": 11625, "UM": "ml", "Cat": "Mechanical", "PV": "Torque Tube"},
        {"Material": "AL-NA2XY-4X185", "Cantitate": 2800, "UM": "ml", "Cat": "AC Electrical", "PV": "AC Power Cable"},
        {"Material": "AL-CU-M12-185", "Cantitate": 252, "UM": "buc", "Cat": "DC Electrical", "PV": "Electrical Lugs"},
        {"Material": "EMSKV-63-IP68", "Cantitate": 84, "UM": "buc", "Cat": "DC Electrical", "PV": "M63 Gland"},
        {"Material": "GRM-55-400-G", "Cantitate": 450, "UM": "ml", "Cat": "AC Electrical", "PV": "Cable Tray"},
        {"Material": "AC-SW-80OV-630", "Cantitate": 21, "UM": "buc", "Cat": "AC Electrical", "PV": "AC Protection"},
        {"Material": "DC-SOL-6-RED", "Cantitate": 34770, "UM": "ml", "Cat": "DC Electrical", "PV": "Solar Cable Red"},
        {"Material": "DC-SOL-6-BK", "Cantitate": 34770, "UM": "ml", "Cat": "DC Electrical", "PV": "Solar Cable Black"},
        {"Material": "MC4-EVO2-1500V", "Cantitate": 930, "UM": "set", "Cat": "DC Electrical", "PV": "Connectors"},
        {"Material": "IDM-JB-800-MC4", "Cantitate": 465, "UM": "buc", "Cat": "Mechanical", "PV": "Jumper Cable"},
        {"Material": "MC4-Y-ADAPTER", "Cantitate": 105, "UM": "set", "Cat": "DC Electrical", "PV": "Y-Branch"},
        {"Material": "GT-404-GALV-FT", "Cantitate": 3110, "UM": "ml", "Cat": "Earthing", "PV": "Grounding Tape"},
        {"Material": "ER-1500-BP", "Cantitate": 155, "UM": "buc", "Cat": "Earthing", "PV": "Earth Rod"},
        {"Material": "SS-TIE-360-UV", "Cantitate": 17500, "UM": "buc", "Cat": "Consumables", "PV": "Cable Ties"},
        {"Material": "PVC-CONDUIT-32", "Cantitate": 680, "UM": "ml", "Cat": "Consumables", "PV": "Protection Tube"},
        {"Material": "UV-STR-LAB-SEQ", "Cantitate": 465, "UM": "buc", "Cat": "Consumables", "PV": "Identification"},
        {"Material": "TP-8012-YEL", "Cantitate": 7, "UM": "buc", "Cat": "Consumables", "PV": "Marking Tool"}
    ]

    for item in master_bom:
        # Verificam daca materialul exista deja
        query = inv_ref.where("Material", "==", item["Material"]).stream()
        docs = list(query)
        
        data = {
            "Material": item["Material"],
            "Cantitate_Planificata": item["Cantitate"],
            "UM": item["UM"],
            "Categorie": item["Cat"],
            "Cod_PVcase": item["PV"],
            "Status": "PLANIFICAT"
        }
        
        if not docs:
            inv_ref.add(data)
            print(f"🆕 IMPORTAT: {item['Material']} ({item['PV']})")
        else:
            docs[0].reference.update(data)
            print(f"🔄 ACTUALIZAT: {item['Material']}")

if __name__ == "__main__":
    import_missing_items()
