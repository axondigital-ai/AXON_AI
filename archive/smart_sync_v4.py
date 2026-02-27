import google.cloud.firestore as firestore
import os
import unicodedata

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def remove_diacritics(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def smart_sync():
    print("🧠 AXON: Sincronizare v4 (Normalizare & Full Map)...")
    nomenclator = {d.id: d.to_dict() for d in db.collection("axon_nomenclator").stream()}
    inventory = db.collection("axon_inventory").stream()
    
    for item in inventory:
        data = item.to_dict()
        mat_raw = str(data.get("Material", ""))
        mat_norm = remove_diacritics(mat_raw).upper()
        
        new_pv_code = "N/A"
        new_cat = data.get("Categorie", "Uncategorized")
        
        for termen, reguli in nomenclator.items():
            termen_norm = remove_diacritics(termen.replace("_", " ")).upper()
            if termen_norm in mat_norm:
                new_pv_code = reguli["pvcase"]
                new_cat = reguli["cat"]
                break
        
        item.reference.update({
            "Cod_PVcase": new_pv_code,
            "Categorie": new_cat
        })
        print(f"🔄 Actualizat: {mat_raw[:25]}... -> {new_pv_code}")

if __name__ == "__main__":
    smart_sync()
