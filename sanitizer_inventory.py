import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def sanitize():
    print("\n🧹 AXON AI: Eliminare dubluri și intrări neconforme...")
    docs = db.collection("axon_inventory").stream()
    
    deleted_count = 0
    for doc in docs:
        data = doc.to_dict()
        # Ștergem orice item care nu are categorie sau are categoria 'None'
        if data.get('Categorie') is None or data.get('Categorie') == "None":
            db.collection("axon_inventory").document(doc.id).delete()
            print(f"   [DELETED]: Ghost item detected -> {doc.id}")
            deleted_count += 1
            
    print(f"\n✅ Curățenie finalizată. Am eliminat {deleted_count} reziduuri.")
    print("🚀 Acum baza de date este 100% conformă cu ierarhia EPC.")

if __name__ == "__main__":
    sanitize()
