import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def smart_sync():
    print("🧠 AXON: Sincronizare inteligentă în curs...")
    
    # 1. Încărcăm Nomenclatorul
    nomenclator = {d.id: d.to_dict() for d in db.collection("axon_nomenclator").stream()}
    
    # 2. Procesăm Inventarul
    inventory = db.collection("axon_inventory").stream()
    
    for item in inventory:
        data = item.to_dict()
        mat_name = str(data.get("Material", "")).upper()
        
        new_pv_code = "N/A"
        new_cat = data.get("Categorie", "Uncategorized")
        
        # Căutăm potriviri în nomenclator
        for termen, reguli in nomenclator.items():
            # În nomenclator am salvat cu "_" în loc de "/", deci revenim la forma originală pentru căutare
            termen_original = termen.replace("_", "/")
            if termen_original in mat_name:
                new_pv_code = reguli["pvcase"]
                new_cat = reguli["cat"]
                break
        
        item.reference.update({
            "Cod_PVcase": new_pv_code,
            "Categorie": new_cat
        })
        print(f"🔄 Actualizat: {mat_name[:25]}... | {new_pv_code}")

if __name__ == "__main__":
    smart_sync()
