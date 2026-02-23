import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def purge_and_rebuild():
    print("🧹 ETAPA 1: Ștergere inventar poluat (eliminare dubluri)...")
    inv_ref = db.collection("axon_inventory")
    docs = inv_ref.stream()
    for doc in docs:
        doc.reference.delete()
    print("✅ Inventar curățat complet.")

    print("\n📦 ETAPA 2: Import Master BOM (Sursa de Adevăr - 25 repere)...")
    # Datele extrase direct din Devizul tău de 2.16 mil EUR
    master_data = [
        # Major Assets
        {"Material": "LR7-72HGD-685M", "PV": "PV Module", "Cat": "Major Assets", "Cant": 11625, "UM": "buc"},
        {"Material": "SUN2000-330KTL-H1", "PV": "Inverter", "Cat": "Major Assets", "Cant": 21, "UM": "buc"},
        {"Material": "STS-7000K-H1", "PV": "Transformer Station", "Cat": "Major Assets", "Cant": 1, "UM": "unit"},
        {"Material": "SmartLogger3000B", "PV": "Communication Unit", "Cat": "Major Assets", "Cant": 1, "UM": "buc"},
        
        # Mechanical (Ideamatec)
        {"Material": "IDM-LTEC-1P-75", "PV": "Tracker Unit", "Cat": "Mechanical", "Cant": 155, "UM": "set"},
        {"Material": "IDM-DRV-LTEC-C", "PV": "Drive System", "Cat": "Mechanical", "Cant": 155, "UM": "set"},
        {"Material": "IDM-PILE-C120", "PV": "Foundation", "Cat": "Mechanical", "Cant": 1085, "UM": "buc"},
        {"Material": "IDM-MC-35-EPDM", "PV": "Module Clamp", "Cat": "Mechanical", "Cant": 46500, "UM": "buc"},
        {"Material": "IDM-TT-OCT-80", "PV": "Torque Tube", "Cat": "Mechanical", "Cant": 11625, "UM": "ml"},
        {"Material": "IDM-JB-800-MC4", "PV": "Jumper Cable", "Cat": "Mechanical", "Cant": 465, "UM": "buc"},

        # Electrical DC
        {"Material": "DC-SOL-6-RED", "PV": "Solar Cable Red", "Cat": "DC Electrical", "Cant": 34770, "UM": "ml"},
        {"Material": "DC-SOL-6-BK", "PV": "Solar Cable Black", "Cat": "DC Electrical", "Cant": 34770, "UM": "ml"},
        {"Material": "MC4-EVO2-1500V", "PV": "Connectors", "Cat": "DC Electrical", "Cant": 930, "UM": "set"},
        {"Material": "MC4-Y-ADAPTER", "PV": "Y-Branch", "Cat": "DC Electrical", "Cant": 105, "UM": "set"},
        {"Material": "EMSKV-63-IP68", "PV": "M63 Gland", "Cat": "DC Electrical", "Cant": 84, "UM": "buc"},

        # Electrical AC
        {"Material": "AL-NA2XY-4X185", "PV": "AC Power Cable", "Cat": "AC Electrical", "Cant": 2800, "UM": "ml"},
        {"Material": "GRM-55-400-G", "PV": "Cable Tray", "Cat": "AC Electrical", "Cant": 450, "UM": "ml"},
        {"Material": "AC-SW-80OV-630", "PV": "AC Protection", "Cat": "AC Electrical", "Cant": 21, "UM": "buc"},
        {"Material": "AL-CU-M12-185", "PV": "Electrical Lugs", "Cat": "DC Electrical", "Cant": 252, "UM": "buc"},

        # Earthing
        {"Material": "GT-404-GALV-FT", "PV": "Grounding Tape", "Cat": "Earthing", "Cant": 3110, "UM": "ml"},
        {"Material": "ER-1500-BP", "PV": "Earth Rod", "Cant": 155, "UM": "buc", "Cat": "Earthing", "PV": "Earth Rod"},

        # Consumables
        {"Material": "SS-TIE-360-UV", "PV": "Cable Ties", "Cat": "Consumables", "Cant": 17500, "UM": "buc"},
        {"Material": "PVC-CONDUIT-32", "PV": "Protection Tube", "Cat": "Consumables", "Cant": 680, "UM": "ml"},
        {"Material": "UV-STR-LAB-SEQ", "PV": "Identification", "Cat": "Consumables", "Cant": 465, "UM": "buc"},
        {"Material": "TP-8012-YEL", "PV": "Marking Tool", "Cat": "Consumables", "Cant": 7, "UM": "buc"}
    ]

    for item in master_data:
        inv_ref.add({
            "Material": item["Material"],
            "Cod_PVcase": item["PV"],
            "cod_pvcase": item["PV"], # Dublăm pentru compatibilitate UI
            "Categorie": item["Cat"],
            "Cantitate_Planificata": item["Cant"],
            "Cantitate_Receptionata": item["Cant"], # Presupunem receptie totala pentru audit
            "Cantitate_Instalata": 0,
            "Cantitate_Custodie": 0,
            "UM": item["UM"],
            "Status": "STOC_CENTRAL"
        })
        print(f"📦 Adăugat: {item['Material']} -> {item['PV']}")

if __name__ == "__main__":
    purge_and_rebuild()
