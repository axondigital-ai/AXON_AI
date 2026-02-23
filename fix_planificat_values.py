import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def sync_plan():
    print("🎯 AXON: Sincronizare valori planificate pentru procente...")
    target_values = {
        "IDM-PILE-C120": 1085,
        "IDM-TRK-S1": 44,
        "LR7-72HGD-685M": 11625,
        "SUN2000-330KTL-H1": 40
    }
    
    docs = db.collection("axon_inventory").stream()
    for doc in docs:
        d = doc.to_dict()
        mat_full = str(d.get("Material", ""))
        # Extragem numele de bază pentru a potrivi și Master și Lot
        mat_base = mat_full.split(" (")[0].strip()
        
        if mat_base in target_values:
            # Doar Master Record-ul (cel fără paranteze) trebuie să aibă Planificat-ul total
            # pentru a evita dublarea sumei la grupare
            if "(" not in mat_full:
                doc.reference.update({"Cantitate_Planificata": target_values[mat_base]})
                print(f"✅ Master {mat_base}: Planificat setat la {target_values[mat_base]}")
            else:
                # Loturile contractorilor au planificat 0 (ei doar consumă din master)
                doc.reference.update({"Cantitate_Planificata": 0})

sync_plan()
