import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def audit():
    print(f"\n{'MATERIAL':<30} | {'CAT':<15} | {'PVCASE':<20} | {'STATUS UI'}")
    print("-" * 85)
    
    # Categoriile pe care le afișează interfața ta
    allowed_cats = ['Major Assets', 'Mechanical', 'DC Electrical', 'AC Electrical', 'Earthing', 'Consumables']
    
    docs = db.collection("axon_inventory").stream()
    total = 0
    invisible = 0
    
    for doc in docs:
        d = doc.to_dict()
        mat = d.get("Material", "N/A")[:30]
        cat = d.get("Categorie", "N/A")
        pv = d.get("Cod_PVcase", "N/A")
        
        status = "✅ VIZIBIL" if cat in allowed_cats else "❌ INVIZIBIL (Cat. gresita)"
        if status.startswith("❌"): invisible += 1
        
        print(f"{mat:<30} | {cat:<15} | {pv:<20} | {status}")
        total += 1
    
    print("-" * 85)
    print(f"Total articole în DB: {total}")
    print(f"Articole care NU apar în UI: {invisible}")
    if total < 50:
        print("\n💡 NOTĂ: Ai puține articole. Probabil trebuie să IMPORTĂM restul din fișierul BOM.")

if __name__ == "__main__":
    audit()
