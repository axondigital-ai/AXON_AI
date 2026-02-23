import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def apply_visual_logic():
    print("\n🎨 AXON CORE: Aplicare logică vizuală pe materiale...")
    inv_ref = db.collection("axon_inventory").stream()
    
    # Echipamentele care rămân la "Nivel 1" (Vizibile imediat)
    master_items = ["LR7-72HGD-685M", "SUN2000-330KTL-H1", "STS-7000K-H1", "IDM-H1P-TRACK"]

    for doc in inv_ref:
        level = 1 if doc.id in master_items else 2
        db.collection("axon_inventory").document(doc.id).update({
            "Nivel_Vizibilitate": level,
            "Afisare_Logica": "Principala" if level == 1 else "Detaliu"
        })
    print("✅ [LOGICĂ APLICATĂ]: Materialele au acum ierarhie de afișare.")

if __name__ == "__main__":
    apply_visual_logic()
