import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def repair():
    print("🛠️ AXON REPAIR: Sincronizare forțată Trackers...")
    docs = db.collection("axon_inventory").stream()
    
    found_master = False
    found_lot = False

    for doc in docs:
        d = doc.to_dict()
        mat = str(d.get("Material", ""))
        
        # Căutăm orice are legătură cu tracker-ul IDM-TRK-S1
        if "IDM-TRK-S1" in mat:
            # Forțăm categoria exactă și curățăm numele
            new_data = {
                "Categorie": "Major Assets",
                "Material": mat.strip()
            }
            doc.reference.update(new_data)
            
            if "(" in mat:
                found_lot = True
                print(f"✅ Lot detectat și reparat: {mat}")
            else:
                found_master = True
                print(f"✅ Master detectat și reparat: {mat}")

    if not found_master:
        print("⚠️ Master Record lipsește! Îl recreăm acum...")
        db.collection("axon_inventory").add({
            "Material": "IDM-TRK-S1",
            "Categorie": "Major Assets",
            "Cantitate_Planificata": 44,
            "Cantitate_Receptionata": 44,
            "Cantitate_Custodie": 0,
            "Cantitate_Validata": 0,
            "Status": "RECONSTRUIT"
        })

repair()
