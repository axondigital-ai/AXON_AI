import google.cloud.firestore as firestore
import os
import unicodedata

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def clean_text(t):
    t = str(t).upper()
    nfkd_form = unicodedata.normalize('NFKD', t)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def sync():
    print("🚀 AXON MASTER SYNC: Forțare date în Inventar...")
    
    # 1. Luăm regulile
    rules = {d.id: d.to_dict() for d in db.collection("axon_nomenclator").stream()}
    
    # 2. Actualizăm inventarul
    inv_docs = db.collection("axon_inventory").stream()
    
    for doc in inv_docs:
        data = doc.to_dict()
        mat_raw = data.get("Material", "")
        mat_clean = clean_text(mat_raw)
        
        final_pv = "N/A"
        final_cat = data.get("Categorie", "Uncategorized")
        
        for termen, r in rules.items():
            if clean_text(termen) in mat_clean:
                final_pv = r["pvcase"]
                final_cat = r["cat"]
                break
        
        # Scrim în ambele variante de nume de câmp pentru siguranță
        doc.reference.update({
            "Cod_PVcase": final_pv,
            "cod_pvcase": final_pv,
            "Categorie": final_cat
        })
        print(f"✔️ {mat_clean[:20]} -> {final_pv}")

if __name__ == "__main__":
    sync()
