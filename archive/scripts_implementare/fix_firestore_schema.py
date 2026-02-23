import google.cloud.firestore as firestore
import os

PROJECT_ID = "axon-core-os"
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
db = firestore.Client(project=PROJECT_ID)

def align_dna_to_v108():
    print("🔧 AXON DATA ALIGNMENT: Aliniem baza de date cu v10.8...")
    protocols = db.collection("axon_protocols").stream()
    
    for doc in protocols:
        data = doc.to_dict()
        # Dacă câmpul 'content' lipsește, îl creăm din celelalte date
        if "content" not in data:
            # Combinăm tot ce am scris noi nou într-un singur text lung (string)
            new_content = ""
            for key, value in data.items():
                if key != "content":
                    new_content += f"{key.upper()}: {value}\n"
            
            db.collection("axon_protocols").document(doc.id).update({
                "content": new_content
            })
            print(f"✅ Aliniat protocol: {doc.id}")
        else:
            print(f"ℹ️ Protocolul {doc.id} are deja câmpul 'content'.")

if __name__ == "__main__":
    align_dna_to_v108()
