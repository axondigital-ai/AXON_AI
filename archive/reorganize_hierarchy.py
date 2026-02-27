import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def reorganize():
    print("\n🧬 AXON AI: Implementare Vizualizare Logică (Hierarchical View)...")
    
    inventory_ref = db.collection("axon_inventory").stream()
    
    for item in inventory_ref:
        data = item.to_dict()
        cod = item.id
        
        # Definim logica de prioritizare (Level 1 = Principal, Level 2 = Detaliu)
        priority = 2
        main_equipment_codes = [
            "LR7-72HGD-685M", "SUN2000-330KTL-H1", "STS-7000K-H1", 
            "IDM-H1P-TRACK", "CAB-SOLAR-6-TOT", "AL-NA2XY-4X185"
        ]
        
        if cod in main_equipment_codes:
            priority = 1 # Acestea vor apărea primele în liste
            
        db.collection("axon_inventory").document(cod).update({
            "Level": priority,
            "View_Type": "Executive" if priority == 1 else "Detailed"
        })
        
    print("✅ [REORGANIZAT]: Vizualizarea este acum ierarhizată (Principal -> Detaliu).")

if __name__ == "__main__":
    reorganize()
