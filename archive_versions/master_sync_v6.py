import google.cloud.firestore as firestore
import os
import unicodedata

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def normalize_string(t):
    t = str(t).upper().replace("_", " ").replace("-", " ")
    nfkd_form = unicodedata.normalize('NFKD', t)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).strip()

def sync():
    print("🚀 AXON MASTER SYNC v6: Pornire mapare elastică...")
    
    rules = {d.id: d.to_dict() for d in db.collection("axon_nomenclator").stream()}
    inv_docs = db.collection("axon_inventory").stream()
    
    for doc in inv_docs:
        data = doc.to_dict()
        mat_raw = data.get("Material", "")
        mat_norm = normalize_string(mat_raw)
        
        final_pv = "N/A"
        final_cat = data.get("Categorie", "Uncategorized")
        
        # Căutăm cea mai bună potrivire
        for termen_id, r in rules.items():
            termen_search = normalize_string(r["termen"])
            if termen_search in mat_norm:
                final_pv = r["pvcase"]
                final_cat = r["cat"]
                break
        
        doc.reference.update({
            "Cod_PVcase": final_pv,
            "cod_pvcase": final_pv,
            "Categorie": final_cat
        })
        print(f"✔️ {mat_norm[:20]}... -> {final_pv}")

if __name__ == "__main__":
    sync()
