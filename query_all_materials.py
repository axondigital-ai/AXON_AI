import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def get_inventory_list():
    print("\n📋 LISTĂ MASTER MATERIALE - AXON CORE")
    print("-" * 80)
    print(f"{'MATERIAL CODE':<25} | {'CATEGORIE':<15} | {'PLANIFICAT':<12} | {'STATUS'}")
    print("-" * 80)
    
    docs = db.collection("axon_inventory").stream()
    
    count = 0
    for doc in docs:
        d = doc.to_dict()
        mat = d.get("Material", "N/A")
        cat = d.get("Categorie", "N/A")
        plan = d.get("Cantitate_Planificata", 0)
        stat = d.get("Status", "N/A")
        
        print(f"{mat:<25} | {cat:<15} | {plan:<12} | {stat}")
        count += 1
    
    print("-" * 80)
    print(f"Total repere identificate: {count}")

if __name__ == "__main__":
    get_inventory_list()
