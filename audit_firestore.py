import google.cloud.firestore as firestore
import os

# Configurare Proiect
os.environ["GOOGLE_CLOUD_PROJECT"] = "axon-core-os"
db = firestore.Client()

def inspect_content_field():
    print("\n🔍 AUDIT DE CONȚINUT FIRESTORE (AXON)")
    print("-" * 50)
    
    protocols = db.collection("axon_protocols").stream()
    
    for doc in protocols:
        data = doc.to_dict()
        print(f"\n📄 Agent: {doc.id}")
        
        if "content" in data:
            val = data["content"]
            print(f"   [TIP DATA]: {type(val).__name__}")
            
            if isinstance(val, dict):
                print(f"   ⚠️ ATENȚIE: 'content' este un DICȚIONAR, nu un STRING!")
                print(f"   [CHEI INTERNE]: {list(val.keys())}")
            else:
                preview = str(val)[:100].replace('\n', ' ')
                print(f"   [PREVIEW]: {preview}...")
        else:
            print("   ❌ EROARE: Câmpul 'content' LIPSEȘTE!")
            print(f"   [CHEI DISPONIBILE]: {list(data.keys())}")

if __name__ == "__main__":
    inspect_content_field()
