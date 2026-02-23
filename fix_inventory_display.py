import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def fix_display():
    print("\n🔍 AXON AI: Restaurare vizibilitate cantități pentru v10.8...")
    inventory_ref = db.collection("axon_inventory").stream()
    
    count = 0
    for item in inventory_ref:
        data = item.to_dict()
        # Verificăm dacă avem noua structură și lipsesc datele din cea veche
        if "Cantitate_Planificata" in data:
            db.collection("axon_inventory").document(item.id).update({
                "Cantitate": data["Cantitate_Planificata"] # Mapăm pentru interfață
            })
            count += 1

    print(f"✅ [REPARAT]: {count} linii au fost mapate corect pentru afișare.")
    print("💡 Verifică acum Tab-ul Gestiune în interfață.")

if __name__ == "__main__":
    fix_display()
