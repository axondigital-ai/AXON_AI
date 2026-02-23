import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def run_detailed_audit():
    print("\n🔍 [AUDIT GESTIUNE AXON - PROIECT ROGVAIV]")
    print("=" * 90)
    
    docs = db.collection("axon_inventory").stream()
    
    # Organizăm datele în memorie pentru a le afișa ordonat
    inventory_data = []
    for doc in docs:
        inventory_data.append(doc.to_dict())
    
    # Sortăm după Categorie
    categories = sorted(list(set(item.get('Categorie', 'Neclasificat') for item in inventory_data)))
    
    for cat in categories:
        print(f"\n📁 CATEGORIE: {cat}")
        print(f"{'COD':<20} | {'DESCRIERE':<40} | {'CANTITATE':<15} | {'UM':<5}")
        print("-" * 90)
        
        items_in_cat = [i for i in inventory_data if i.get('Categorie') == cat]
        for item in items_in_cat:
            cod = item.get('Cod_Material', 'N/A')
            nume = item.get('Material', 'N/A')[:40]
            # Folosim 'Cantitate' pentru compatibilitate v10.8
            qty = item.get('Cantitate', 0)
            um = item.get('UM', 'buc')
            print(f"{cod:<20} | {nume:<40} | {qty:<15,} | {um:<5}")
            
    print("\n" + "=" * 90)
    print(f"✅ Audit finalizat. Total repere înregistrate: {len(inventory_data)}")

if __name__ == "__main__":
    run_detailed_audit()
