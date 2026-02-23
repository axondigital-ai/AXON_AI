import google.cloud.firestore as firestore
import os

os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def deep_clean():
    print("🧹 AXON: Se inițiază curățarea generală a bazei de date...")
    inv_ref = db.collection("axon_inventory")
    docs = inv_ref.stream()
    
    deleted_count = 0
    reset_count = 0

    for doc in docs:
        data = doc.to_dict()
        material_name = data.get("Material", "")
        
        # 1. Ștergem loturile create pentru contractori (cele care conțin paranteze sau 'Lot')
        if "(" in material_name or "Lot" in material_name or doc.id.startswith("LOT_"):
            doc.reference.delete()
            deleted_count += 1
        else:
            # 2. Resetăm valorile pentru articolele Master
            doc.reference.update({
                "Cantitate_Receptionata": 0,
                "Cantitate_Custodie": 0,
                "Cantitate_Instalata": 0, # Coloana 'Raportat Constructor'
                "Cantitate_Validata": 0,  # Coloana 'Validat PM'
                "Status": "PLANIFICAT",
                "Contractor_Custodie": ""
            })
            reset_count += 1

    print(f"✅ Curățenie finalizată!")
    print(f"🗑️ Loturi de test șterse: {deleted_count}")
    print(f"🔄 Articole Master resetate la zero: {reset_count}")

if __name__ == "__main__":
    deep_clean()
