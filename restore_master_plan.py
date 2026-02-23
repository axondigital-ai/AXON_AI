import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def restore():
    print("🛠️ AXON: Restaurare Cantități Planificate (BOM Master)...")
    
    # Valorile corecte din BOM/Deviz
    bom_values = {
        "LR7-72HGD-685M": 11625, "SUN2000-330KTL-H1": 21, "STS-7000K-H1": 1,
        "IDM-PILE-C120": 1085, "IDM-MC-35-EPDM": 46500, "IDM-TT-OCT-80": 11625,
        "AL-NA2XY-4X185": 2800, "DC-SOL-6-RED": 34770, "DC-SOL-6-BK": 34770
    }

    docs = db.collection("axon_inventory").stream()
    for doc in docs:
        data = doc.to_dict()
        mat_base = data.get("Material", "").split(" (")[0] # Luăm numele de bază fără "(Lot...)"
        
        if mat_base in bom_values:
            # Restaurăm planul doar pe înregistrarea principală (cea fără "Lot")
            if "Lot" not in data.get("Material", ""):
                doc.reference.update({"Cantitate_Planificata": bom_values[mat_base]})
            else:
                # Loturile secundare au mereu planificare 0 pentru a nu dubla sumele la centralizare
                doc.reference.update({"Cantitate_Planificata": 0})
    print("✅ Planificare restaurată.")

if __name__ == "__main__":
    restore()
